
import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        message="CI/CD practice application",
        version=os.getenv("APP_VERSION", "local")
    )


@app.get("/health")
def health():
    return jsonify(status="healthy"), 200


@app.get("/version")
def version():
    return jsonify(version=os.getenv("APP_VERSION", "local")), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
