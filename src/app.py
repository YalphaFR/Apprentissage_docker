from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Fonction pour créer une connexion PostgreSQL
def get_conn():
    return psycopg2.connect(
        dbname="workshop",
        user="admin",
        password="secret",
        host="db",
        port=5432
    )

# Route health
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# Route pour récupérer tous les items
@app.route("/api/items", methods=["GET"])
def get_items():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, name FROM items ORDER BY id;")
            items = cur.fetchall()
    return jsonify({"items": items}), 200

# Route pour insérer un nouvel item
@app.route("/api/insert", methods=["POST"])
def insert_item():
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Génère automatiquement le nom en fonction du dernier ID
            cur.execute("SELECT MAX(id) FROM items;")
            max_id = cur.fetchone()[0] or 0
            new_name = f"Item {max_id + 1}"

            cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id;", (new_name,))
            inserted_id = cur.fetchone()[0]
            conn.commit()

    return jsonify({"message": "Item inserted", "id": inserted_id}), 201

if __name__ == "__main__":
    # Serveur sur toutes les interfaces sur le port 8080
    app.run(host="0.0.0.0", port=8080)