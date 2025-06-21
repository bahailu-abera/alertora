from app.extensions import mongo_database
from app.utils.redis_utils import cache_auth_token, get_cached_client_id


def verify_api_token(api_token):
    client_id = get_cached_client_id(api_token)
    if client_id:
        return client_id

    client = mongo_database.clients.find_one({"api_token": api_token})
    if client:
        client_id = str(client["_id"])
        cache_auth_token(api_token, client_id)
        return client_id

    return None
