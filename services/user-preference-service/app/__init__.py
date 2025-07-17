from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_redis import FlaskRedis
from .config import Config
import os


def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(base_dir, "web", "templates")
    static_dir = os.path.join(base_dir, "web", "static")

    app = Flask(
        __name__, template_folder=templates_dir, static_folder=static_dir
    )

    app.config.from_object(Config)

    CORS(app, origins=["https://alertora.addisalem.xyz"])

    from app import extensions

    extensions.mongo_database = PyMongo(app).cx["alertora"]
    extensions.redis_client = FlaskRedis(app)

    from app.api.v1.routes.get_preference import preference_get_bp
    from app.api.v1.routes.update_preference import preference_update_bp
    from app.web.routes.preference_page import web_bp

    app.register_blueprint(preference_get_bp, url_prefix="/api/v1")
    app.register_blueprint(preference_update_bp, url_prefix="/api/v1")
    app.register_blueprint(web_bp)

    return app
