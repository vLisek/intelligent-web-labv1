import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Wczytanie bazy z csv i załatanie braków w opisach
df = pd.read_csv("movies.csv")
df["overview"] = df["overview"].fillna("")

# Budowa macierzy TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])

# Wyliczenie macierzy podobieństw
sim_matrix = cosine_similarity(tfidf_matrix)


def recommend(title, top_n=5, genre=None):
    # Znalezienie id wiersza
    match = df[df["title"].str.lower() == title.lower()]

    if match.empty:
        return None

    idx = match.index[0]

    # Wyciągnięcie wyników dla szukanego filmu i ich posortowanie malejąco
    scores = sorted(enumerate(sim_matrix[idx]), key=lambda x: x[1], reverse=True)

    recommendations = []
    # Lecimy po wynikach z pominięciem pętli dla samego siebie -> i != idx
    for i, s in scores:
        if i == idx:
            continue

        # Zabezpieczenie jeśli klient podał filtr 'genre'
        if genre and genre.lower() not in df["genres"][i].lower():
            continue

        # Tworzenie słownika JSON-able
        recommendations.append({
            "title": df["title"][i],
            "genres": df["genres"][i],
            "rating": round(float(df["rating"][i]), 1),
            "score": round(float(s), 3)
        })

        if len(recommendations) >= top_n:
            break

    return recommendations