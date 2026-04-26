from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from app.config import Config

API_VERSION = "v1"

db = SQLAlchemy()

migrate = Migrate()


def create_app():
    """App factory: crea y configura la instancia de Flask."""

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    CORS(app, origins=app.config["CORS_ALLOWED_ORIGINS"])

    @app.route("/health", methods=["GET"])
    def health():
        return {
            "status": "ok",
            "service": "alojamientos-api",
            "version": API_VERSION,
        }, 200

    @app.errorhandler(404)
    def recurso_no_encontrado(error):
        return {"success": False, "error": {"message": "Recurso no encontrado"}}, 404

    @app.errorhandler(500)
    def error_interno(error):
        return {
            "success": False,
            "error": {"message": "Error interno del servidor"},
        }, 500

    return app
