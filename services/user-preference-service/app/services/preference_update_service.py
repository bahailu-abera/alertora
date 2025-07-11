from app.validators.channel_validator import validate_channels
from app.utils.redis_utils import cache_user_preference
from app.utils.mongodb_utils import update_user_preference_document


def update_user_preference(user_id, client_id, channels, allowed_types):
    is_valid, err = validate_channels(channels)
    if not is_valid:
        return {"error": err}, 400

    update_user_preference_document(
        user_id, client_id, channels, allowed_types
    )

    prefence_data = {"channels": channels, "allowed_types": allowed_types}

    cache_user_preference(user_id, client_id, str(prefence_data))

    return {"message": "Preferences updated successfully."}, 200
