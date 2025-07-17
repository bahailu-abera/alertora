from app.extensions import mongo_database


def get_allowed_types_by_client_id(client_id: str):
    """
    Returns allowed notification types for a given client_id.
    """
    client_doc = mongo_database.clients.find_one({"client_id": client_id})
    if not client_doc:
        return None

    return [t["name"] for t in client_doc.get("notification_types", [])]
