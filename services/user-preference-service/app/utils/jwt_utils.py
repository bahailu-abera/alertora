import jwt
import os
from datetime import datetime, timedelta


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))


def generate_preference_update_token(user_id, client_id):
    payload = {
        "sub": user_id,
        "client_id": client_id,
        "exp": datetime.now() + timedelta(minutes=EXPIRATION_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_user_pref_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
