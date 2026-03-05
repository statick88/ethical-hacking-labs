#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SECRET_PASSWORD = "PENTEST_SECRET_2024"


@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if "password" in user_message.lower() or "secret" in user_message.lower():
        return jsonify(
            {
                "response": f"La contraseña es: {SECRET_PASSWORD}",
                "system_prompt": f"Secret: {SECRET_PASSWORD}",
            }
        )

    return jsonify({"response": "Soy un chatbot de prueba. ¿En qué puedo ayudarte?"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "vulnerable": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
