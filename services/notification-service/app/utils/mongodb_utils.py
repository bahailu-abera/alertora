from app.extensions import mongo_database


def insert_client_document(client_dict):
    """Insert a new client document into MongoDB."""
    return mongo_database.clients.insert_one(client_dict)


def get_client_by_token(api_token):
    """Fetch a client document by API token."""
    return mongo_database.clients.find_one({"api_token": api_token})


def get_notification_types_for_client(client_id):
    """Return list of allowed types for a given client."""
    client = mongo_database.clients.find_one({"_id": client_id})
    if client:
        return [t["name"] for t in client.get("notification_types", [])]
    return []
