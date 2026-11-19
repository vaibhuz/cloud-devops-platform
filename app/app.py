from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Cloud DevOps Platform is running!",
        "hostname": socket.gethostname(),
        "status": "success"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200

@app.route("/api/v1/inventory")
def inventory():
    return jsonify({
        "service": "Inventory API",
        "items": [
            {"id": 1, "name": "Laptop", "quantity": 10},
            {"id": 2, "name": "Keyboard", "quantity": 25}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
