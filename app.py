import os
import socket
import psycopg

from flask import Flask, jsonify

app = Flask(__name__)

# Message affiché sur la page d'accueil : à modifier pendant le workshop
MESSAGE = "Bonjour de Prince  depuis mon pipeline !"
# Version injectée au build (SHA du commit en CI, "dev" par défaut)
VERSION = os.getenv("APP_VERSION", "dev")


@app.route("/")
def index():
    return (
        f"<h1>{MESSAGE}</h1>"
        f"<p>Version : <code>{VERSION[:7]}</code></p>"
        f"<p>Conteneur : <code>{socket.gethostname()}</code></p>"
    )


@app.route("/health")
def health():
    return jsonify(status="ok", version=VERSION)

@app.route("/db")
def db():
    try:
        with psycopg.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode="require",
            connect_timeout=5,
        ) as conn:
            version = conn.execute("SELECT version()").fetchone()[0]
        return jsonify(status="ok", database=os.getenv("DB_NAME"), version=version)
    except Exception as e:
        return jsonify(status="erreur", detail=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
