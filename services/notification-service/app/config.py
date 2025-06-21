import os


class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/alertora")
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
    USER_PREF_SERVICE_URL = os.getenv("USER_PREF_SERVICE_URL",
                                      "http://user-preference-service:8001/api/v1/preferences")
