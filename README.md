# Moduł 01 (Rekomendacje)
### Co robi moduł rekomendacji:
System sugeruje filmy w dwóch trybach. Pierwszy analizuje treść i opisy (TF-IDF), proponując tytuły o podobnej tematyce. Drugi wykorzystuje filtrowanie zespołowe (Collaborative Filtering), przewidując oceny na podstawie podobieństwa gustów użytkowników (odchyleń od ich średnich ocen).

### Jak go uruchomić:
Upewnij się, że masz aktywne środowisko wirtualne.
1. Zainstaluj biblioteki komendą `pip install -r requirements.txt`.
2. Następnie uruchom serwer poleceniem `python app.py`.

### Przykładowa odpowiedź API:
Dla zapytania `GET /api/recommend?user=Ania` API zwraca kod `200` oraz JSON: 
`[{"because": ["Klara", "Bartek"], "predicted": 4.31, "title": "Inception"}]`

<hr>

## Exit ticket:

### Laboratorium 1:
**1. Co zrobiliśmy sami?**
Skonfigurowaliśmy środowisko wirtualne, napisaliśmy nową logikę w Pythonie i fizycznie zarządzaliśmy repozytorium w modelu Git Flow (tworzenie branchy z inicjałami, robienie commitów, łączenie kodu przez Pull Requesty). Sami testowaliśmy działanie API w przeglądarce i generowaliśmy pliki instalacyjne (requirements.txt).

**2. W czym pomogło AI?** 
AI pełniło rolę nawigatora przy troubleshootingu – tłumaczyło niezrozumiałe błędy w terminalu (np. brakujące pakiety, błędy środowiska) oraz podpowiadało, jak poprawnie zsynchronizować lokalne repozytorium, gdy utworzyliśmy brancha w złym momencie. Dodatkowo AI pokazało, jak użyć modułu request z Flaska do obsługi parametrów URL.

**3. Czego jeszcze nie rozumiemy?**
Jak dokładnie działa pamięć podręczna w takim środowisku – co stałoby się ze słownikiem PRODUCTS, gdyby dwóch klientów wywołało metodę POST dodającą nowy produkt w dokładnie tej samej mikrosekundzie?

<hr>

### Laboratorium 2:
**JEDNO, CO DZIAŁA:**
Zamiana tekstu (opisów filmów) na wektory liczb za pomocą TfidfVectorizer oraz precyzyjne odnajdywanie kątów między nimi (cosine similarity), co dało wiarygodne wyniki podobieństwa.

**JEDNO, CO NIE DZIAŁA:**
Błąd ModuleNotFoundError: No module named 'pandas' przy odpaleniu kodu u drugiej osoby, wynikający z braku synchronizacji lokalnych paczek, oraz konflikt wersji numpy ze starszym Pythonem. Rozwiązaliśmy to przez ręczną doinstalację kompatybilnych bibliotek z requirements.txt.

**JEDEN POMYSŁ:**
Polecanie ofert pracy na portalach rekrutacyjnych – system mógłby szukać podobnych ogłoszeń na podstawie samego opisu stanowiska i wymaganych umiejętności (TF-IDF z tekstów ofert).

<hr>

### Laboratorium 3 (Trzy zdania na drogę):
1. **Filtrowanie zespołowe (CF)** bada podobieństwo między ludźmi poprzez ich oceny, całkowicie ignorując cechy przedmiotu, podczas gdy metoda content-based patrzy tylko na cechy przedmiotu (treść, opisy), ignorując gusta innych ludzi.
2. **Centrowanie ocen** (odejmowanie średniej) sprowadza oceny do wspólnego mianownika – bada, czy film podobał się bardziej niż zwykle, dzięki czemu system poprawnie widzi podobieństwo między surowym krytykiem (średnia 2.0) a łagodnym entuzjastą (średnia 4.5).
3. **Problem (Cold Start):** Algorytm CF jest całkowicie bezużyteczny dla nowo zarejestrowanego użytkownika, który nie wystawił jeszcze żadnej oceny; Netflix naprawia to, prosząc na starcie o wyklikanie kilku ulubionych filmów lub używając metod hybrydowych.