import uuid
import secrets
from app.models.client_model import ClientModel
from app.utils.redis_utils import cache_auth_token
from app.utils.mongodb_utils import insert_client_document
from app.validators.registration_validator import validate_registration_payload


def generate_token():
    return secrets.token_urlsafe(32)


def register_client(data):
    is_valid, error = validate_registration_payload(data)
    if not is_valid:
        return {"error": error}, 400

    service_name = data["service_name"]
    notification_types = data["notification_types"]

    client_id = str(uuid.uuid4())
    api_token = generate_token()

    client = ClientModel(
            client_id=client_id,
            service_name=service_name,
            api_token=api_token,
            notification_types=notification_types
        )
    
    insert_client_document(client.to_dict())
    cache_auth_token(api_token, client_id)

    return {
        "client_id": client_id,
        "api_token": api_token
    }
