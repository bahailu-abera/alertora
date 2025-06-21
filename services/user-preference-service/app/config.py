import os


class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/alertora")
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/1")
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
