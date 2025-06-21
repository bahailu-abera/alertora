import uuid
import secrets
from app.extensions import mongo_database
from app.models.client_model import ClientModel
from app.utils.redis_utils import cache_auth_token


def generate_token():
    return secrets.token_urlsafe(32)


def register_client(data):
    service_name = data.get("service_name")
    notification_types = data.get("notification_types", [])

    if not service_name or not isinstance(notification_types, list):
        return {"error": "Invalid input"}, 400

    client_id = str(uuid.uuid4())
    api_token = generate_token()

    client = ClientModel(
            client_id=client_id,
            service_name=service_name,
            api_token=api_token,
            notification_types=notification_types
        )

    mongo_database.clients.insert_one(
       client.to_dict()
    )

    cache_auth_token(api_token, client_id)

    return {
        "client_id": client_id,
        "api_token": api_token
    }
