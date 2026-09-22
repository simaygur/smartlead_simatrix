import os

from flask import Flask, jsonify
from flask_cors import CORS

from config import config_by_name
from app.database import get_db, init_db
from app.routes import pages_bp, api_bp


def create_app(config_name=None):
    config_name = config_name or os.environ.get("APP_ENV", "development")

    if config_name not in config_by_name:
        raise ValueError(f"Geçersiz APP_ENV değeri: {config_name}")

    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    CORS(app, origins=app.config["CORS_ORIGINS"])

    init_db(app)

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/health")
    def health():
        get_db().execute("SELECT 1").fetchone()

        return jsonify({
            "basari": True,
            "durum": "aktif",
            "ortam": config_name
        })

    return app
