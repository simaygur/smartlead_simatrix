from flask import Flask, jsonify
from flask_cors import CORS

from config import config_by_name
from app.database import init_db
from app.routes import pages_bp, api_bp


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    CORS(app, origins=app.config["CORS_ORIGINS"])

    init_db(app)

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/health")
    def health():
        return jsonify({
            "basari": True,
            "durum": "aktif"
        })

    return app