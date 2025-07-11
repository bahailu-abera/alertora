from app.utils.redis_utils import cache_user_preference
from app.utils.redis_utils import get_cached_user_preference
from app.utils.mongodb_utils import get_user_preference_document
import ast


def get_user_preference(user_id, client_id):
    cached = get_cached_user_preference(user_id, client_id)
    if cached:
        return {"preferences": ast.literal_eval(cached)}, 200

    doc = get_user_preference_document(user_id)
    if not doc:
        return {"message": "No preferences found for this user."}, 404

    prefs = doc.get("preferences", {}).get(client_id)
    if not prefs:
        return {"message": "No preferences set for this client."}, 404

    cache_user_preference(user_id, client_id, str(prefs))

    return {"preferences": prefs}, 200
