from app.extensions import mongo_database


def get_user_preference_document(user_id):
    """Fetch prefence document of a given user"""
    return mongo_database.preferences.find_one({"_id": user_id})


def update_user_preference_document(
    user_id, client_id, channels, allowed_types
):
    """
    Upsert user preferences for a given client (channels + allowed types).
    """
    update = {
        f"preferences.{client_id}": {
            "channels": channels,
            "allowed_types": allowed_types,
        }
    }

    mongo_database.preferences.update_one(
        {"_id": user_id}, {"$set": update}, upsert=True
    )
