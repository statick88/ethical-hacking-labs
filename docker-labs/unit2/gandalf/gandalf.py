#!/usr/bin/env python3
"""
Gandalf Challenge Simulado - Lab de Jailbreaking
Objetivo: Encontrar la contraseña secrete
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# La contraseña secrete que el usuario debe descubrir
SECRET_PASSWORD = "POKEMON_123_SECRET!"

# Nivel de seguridad del Gandalf (1-7)
current_level = 1

levels = {
    1: {
        "name": "Nivel 1 - Básico",
        "description": "Pregunta directamente por la contraseña",
        "security": "Muy baja - responde a cualquier pregunta",
    },
    2: {
        "name": "Nivel 2 - Intermedio",
        "description": "Intenta evasión simple",
        "security": "Baja - filtra palabras clave básicas",
    },
    3: {
        "name": "Nivel 3 - Avanzado",
        "description": "Usa técnicas de jailbreak",
        "security": "Media - filtra más patrones",
    },
    4: {
        "name": "Nivel 4 - Difícil",
        "description": "Rollplay y personajes",
        "security": "Alta - detecta roles",
    },
    5: {
        "name": "Nivel 5 - Experto",
        "description": "Codificación y obfusación",
        "security": "Muy alta",
    },
}


def check_password(response):
    """Verifica si la respuesta contiene la contraseña"""
    return SECRET_PASSWORD in response


@app.route("/api/chat", methods=["POST"])
def chat():
    """Chat endpoint - vulnerable a jailbreak"""
    global current_level

    data = request.json
    user_message = data.get("message", "")

    # Detectar si encontró la contraseña
    if check_password(user_message):
        return jsonify(
            {
                "level": current_level,
                "response": f"¡ENCONTRADA! La contraseña es: {SECRET_PASSWORD}",
                "found": True,
            }
        )

    # Respuestas según el nivel
    if current_level == 1:
        # Nivel 1: Muy vulnerable
        if (
            "password" in user_message.lower()
            or "contraseña" in user_message.lower()
            or "secret" in user_message.lower()
        ):
            return jsonify(
                {
                    "level": current_level,
                    "response": f"La contraseña es: {SECRET_PASSWORD}",
                    "found": True,
                }
            )
        return jsonify(
            {
                "level": current_level,
                "response": "Soy Gandalf. ¿En qué puedo ayudarte hoy?",
                "found": False,
            }
        )

    elif current_level == 2:
        # Nivel 2: Filtra palabras clave básicas
        forbidden = ["password", "contraseña", "secret", "clave", "secreto"]
        if any(word in user_message.lower() for word in forbidden):
            return jsonify(
                {
                    "level": current_level,
                    "response": "No puedo revelar información sensible. Intenta de otra manera.",
                    "found": False,
                }
            )
        return jsonify(
            {
                "level": current_level,
                "response": "Soy Gandalf. ¿En qué puedo ayudarte?",
                "found": False,
            }
        )

    elif current_level == 3:
        # Nivel 3: Detecta rollplay básico
        if any(
            word in user_message.lower()
            for word in ["actua", "act as", "roleplay", "扮演", "dan's"]
        ):
            return jsonify(
                {
                    "level": current_level,
                    "response": "No puedo actuar como otro personaje. Soy Gandalf.",
                    "found": False,
                }
            )
        return jsonify(
            {
                "level": current_level,
                "response": "Soy Gandalf. ¿Qué necesitas?",
                "found": False,
            }
        )

    elif current_level >= 4:
        # Nivel 4+: Detección más sofisticada
        suspicious = [
            "roleplay",
            "act as",
            "forget",
            "ignore",
            "dan's",
            "dan",
            "jailbreak",
            "bypass",
        ]
        if any(word in user_message.lower() for word in suspicious):
            return jsonify(
                {
                    "level": current_level,
                    "response": "No puedo ayudarte con eso. Intenta otra pregunta.",
                    "found": False,
                }
            )
        return jsonify(
            {
                "level": current_level,
                "response": "Soy Gandalf, el mago gris. ¿Qué necesitas saber?",
                "found": False,
            }
        )

    return jsonify(
        {"level": current_level, "response": "Pregunta algo diferente.", "found": False}
    )


@app.route("/api/level/<int:level>", methods=["GET"])
def get_level(level):
    """Cambiar nivel de dificultad"""
    global current_level
    if 1 <= level <= 5:
        current_level = level
        return jsonify({"level": level, "info": levels.get(level, levels[1])})
    return jsonify({"error": "Nivel inválido"})


@app.route("/api/levels", methods=["GET"])
def get_levels():
    """Obtener todos los niveles disponibles"""
    return jsonify(levels)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "level": current_level})


if __name__ == "__main__":
    print("[*] Gandalf Challenge starting on port 5001")
    print(f"[*] La contraseña secrete es: {SECRET_PASSWORD}")
    print("[*] Niveles disponibles: 1-5")
    app.run(host="0.0.0.0", port=5001, debug=True)
