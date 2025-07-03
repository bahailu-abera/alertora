from flask import Flask
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from .config import Config
import logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    from app import extensions
    extensions.mongo_database = PyMongo(app).cx['alertora']
    extensions.redis_client = FlaskRedis(app)

    from app.api.v1.routes.get_preference import preference_get_bp
    from app.api.v1.routes.update_preference import preference_update_bp
    from app.web.routes.preference_page import web_bp

    app.register_blueprint(preference_get_bp, url_prefix='/api/v1/preferences')
    app.register_blueprint(preference_update_bp, url_prefix='/api/v1/preferences')
    app.register_blueprint(web_bp)


    return app
