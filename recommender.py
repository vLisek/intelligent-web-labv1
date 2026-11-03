import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Wczytanie bazy ocen i tworzenie macierzy
df = pd.read_csv("ratings.csv")
matrix = df.pivot_table(index="user", columns="title", values="rating")

# Wyśrodkowanie ocen, by poprawnie wyłapać odchylenia od gustu
means = matrix.mean(axis=1)  # średnia ocena każdego użytkownika
centered = matrix.sub(means, axis=0).fillna(0)

# Liczymy podobieństwo (cosine similarity) odchyleń gustu
sim = pd.DataFrame(cosine_similarity(centered), index=matrix.index, columns=matrix.index)


def recommend(user, top_n=5, k=3):
    if user not in matrix.index:
        return None

    # Sortujemy znajomych/sąsiadów od najbardziej podobnego i bierzemy K najbliższych
    neighbors = sim[user].drop(user).sort_values(ascending=False).head(k)

    scores = {}

    # Przechodzimy przez wszystkie filmy w bazie
    for movie in matrix.columns:
        # Jeśli nasz klient już ocenił/oglądał ten film, pomijamy go (szukamy NaN)
        if not pd.isna(matrix.loc[user, movie]):
            continue

        num, den = 0.0, 0.0

        # Pytamy k-najbliższych sąsiadów o ten konkretnie nieoglądany przez klienta film
        for other, weight in neighbors.items():
            r = matrix.loc[other, movie]
            if not pd.isna(r):  # Jeśli sąsiad też to widział
                num += weight * (r - means[other])  # Waga podobieństwa razy różnica gustu sąsiada
                den += abs(weight)  # Sumujemy wagę podobieństwa (na minus lub plus - abs to wartość bezwzględna)

        # Składamy wyniki i przewidujemy ocenę z przedziału 1.0 do 5.0
        if den > 0:
            predicted_rating = means[user] + (num / den)
            scores[movie] = max(1.0, min(5.0, predicted_rating))

    # Sortujemy nasze wyliczenia od najlepszego filmu i przycinamy listę do top_n
    best = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Pakujemy odpowiedź na kształt pożądanego w instrukcji JSONa
    return [{"title": t,
             "predicted": round(float(s), 2),
             "because": [o for o, w in neighbors.items() if not pd.isna(matrix.loc[o, t])]}
            for t, s in best]