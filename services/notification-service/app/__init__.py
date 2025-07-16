from flask import Flask
from .config import Config
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
import logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    from app import extensions

    extensions.mongo_database = PyMongo(app).cx["alertora"]
    extensions.redis_client = FlaskRedis(app)

    from app.api.v1.routes.registration import registration_bp
    from app.api.v1.routes.notify import notify_bp

    app.register_blueprint(registration_bp, url_prefix="/api/v1")
    app.register_blueprint(notify_bp, url_prefix="/api/v1")

    return app
