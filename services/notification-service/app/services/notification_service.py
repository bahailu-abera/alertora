import requests
from app.services.auth_service import verify_api_token
from app.utils.kafka_producer import send_to_kafka
from app.validators.notification_validator import validate_notification_payload
from app.config import Config


def process_notification(data, token):
    """Process an incoming notification request."""

    client_id = verify_api_token(token)
    if not client_id:
        return {"error": "Unauthorized"}, 401

    is_valid, error = validate_notification_payload(data)
    if not is_valid:
        return {"error": error}, 400

    try:
        # Query user preference service
        resp = requests.get(
            Config.USER_PREF_SERVICE_URL,
            params={"user_id": data["recipient_id"], "client_id": client_id},
            timeout=5
        )

        if resp.status_code == 404:
            # No preferences set — send by default
            pass
        elif resp.status_code != 200:
            return {"error": "Failed to fetch user preferences"}, 502
        else:
            prefs = resp.json().get("preferences", {})
            if data["channel"] not in prefs.get("channels", []) or data[
                "notification_type"
            ] not in prefs.get("allowed_types", []):
                return {"error": "User preference rejected"}, 403

    except Exception as e:
        return {"error": f"Preference service error: {str(e)}"}, 500

    message = {
        k: (v.decode("utf-8") if isinstance(v, bytes) else v)
        for k, v in {
            "client_id": client_id,
            "user_id": data["recipient_id"],
            "notification_type": data["notification_type"],
            "channel": data["channel"],
            "content": data["content"],
        }.items()
    }

    topic = f"{data['channel']}_notifications"
    send_to_kafka(topic, message)

    return {"message": "Notification accepted"}, 202
