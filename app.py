from flask import Flask, jsonify, request
from recommender import recommend

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "nazwa": "Klawiatura mechaniczna", "kategoria": "akcesoria",
     "cena": 349.99, "opis": "Przełączniki hot-swap, podświetlenie RGB"},
    {"id": 2, "nazwa": "Mysz bezprzewodowa", "kategoria": "akcesoria",
     "cena": 129.00, "opis": "Ciche przyciski, 4000 DPI"},
    {"id": 3, "nazwa": "Monitor 27 cali", "kategoria": "monitory",
     "cena": 1099.00, "opis": "Matryca IPS, 144 Hz"},
    {"id": 4, "nazwa": "Słuchawki nauszne", "kategoria": "audio",
     "cena": 449.00, "opis": "ANC, 40 h pracy na baterii"},
    {"id": 5, "nazwa": "Hub USB-C", "kategoria": "akcesoria",
     "cena": 199.00, "opis": "HDMI, 3x USB-A, czytnik SD"},
]

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/products")
def products():
    # Pobranie parametru max_price z zapytania HTTP
    max_price = request.args.get("max_price", type=float)

    if max_price is not None:
        # Zwrócenie tylko tych produktów, które są tańsze lub w tej samej cenie
        filtered_products = [p for p in PRODUCTS if p["cena"] <= max_price]
        return jsonify(filtered_products)

    return jsonify(PRODUCTS)

@app.route("/api/products/<int:product_id>")
def get_product(product_id):
    # Szuka produktu w liście PRODUCTS
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)

    if product is None:
        # Zwraca błąd 404 i JSON, jeśli nie znaleziono
        return jsonify({"error": "Produkt nie zostal znaleziony"}), 404

    return jsonify(product)

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json()

    # Prosta walidacja czy w przesłanym JSON-ie są wymagane pola
    if not data or not "nazwa" in data or not "cena" in data:
        return jsonify({"error": "Brak wymaganych danych (nazwa, cena)"}), 400

    # Wyliczanie nowego ID (najwyższe dotychczasowe + 1)
    new_id = max((p["id"] for p in PRODUCTS), default=0) + 1

    new_product = {
        "id": new_id,
        "nazwa": data["nazwa"],
        "kategoria": data.get("kategoria", "inne"),
        "cena": data["cena"],
        "opis": data.get("opis", "")
    }

    PRODUCTS.append(new_product)
    # Zwracamy dodany produkt i kod 201 Created
    return jsonify(new_product), 201

@app.route("/api/recommend")
def api_recommend():
    # Pobranie parametrów z URL
    title = request.args.get("title")
    top_n = request.args.get("top_n", default=5, type=int)
    genre = request.args.get("genre")  # Filtr dla zadania z wyzwaniem

    # Walidacja: Brak tytułu zwraca błąd 400 (Bad Request)
    if not title:
        return jsonify({"error": "Brak parametru title"}), 400

    # Walidacja: top_n musi być z przedziału 1-10, inaczej wymuszamy domyślne 5
    if not (1 <= top_n <= 10):
        top_n = 5

    # Wywołanie funkcji z recommender.py
    results = recommend(title, top_n, genre)

    # Walidacja: Tytułu nie znaleziono w bazie, zwracamy błąd 404 (Not Found)
    if results is None:
        return jsonify({"error": "Film nie znaleziony w bazie"}), 404

    # Sukces: Zwracamy listę polecanych filmów jako JSON
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)