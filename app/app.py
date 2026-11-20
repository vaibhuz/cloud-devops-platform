import os
import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                price NUMERIC(10,2) NOT NULL DEFAULT 0
            )
        """)
    conn.commit()
    return conn

@app.route("/")
def home():
    return jsonify({"message": "Cloud DevOps Inventory API", "status": "running"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/api/v1/inventory", methods=["GET"])
def get_inventory():
    if not DATABASE_URL:
        return jsonify([])
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, quantity, price::float AS price FROM inventory ORDER BY id DESC")
            return jsonify(cur.fetchall())

@app.route("/api/v1/inventory", methods=["POST"])
def add_inventory():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"error": "Product name is required"}), 400
    try:
        quantity = int(data.get("quantity", 0))
        price = float(data.get("price", 0))
        if quantity < 0 or price < 0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"error": "Quantity and price must be non-negative numbers"}), 400

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO inventory (name, quantity, price)
                   VALUES (%s, %s, %s)
                   RETURNING id, name, quantity, price::float AS price""",
                (name, quantity, price)
            )
            item = cur.fetchone()
    return jsonify(item), 201

@app.route("/api/v1/inventory/<int:item_id>", methods=["PUT"])
def update_inventory(item_id):
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    try:
        quantity = int(data.get("quantity", 0))
        price = float(data.get("price", 0))
        if not name or quantity < 0 or price < 0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"error": "Enter a valid name, quantity and price"}), 400

    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """UPDATE inventory SET name=%s, quantity=%s, price=%s
                   WHERE id=%s
                   RETURNING id, name, quantity, price::float AS price""",
                (name, quantity, price, item_id)
            )
            item = cur.fetchone()
    if not item:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(item)

@app.route("/api/v1/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory(item_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM inventory WHERE id=%s RETURNING id", (item_id,))
            item = cur.fetchone()
    if not item:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"message": "Product deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
