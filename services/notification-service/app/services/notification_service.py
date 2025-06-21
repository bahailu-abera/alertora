from app.services.auth_service import verify_api_token
import requests
from app.utils.kafka_producer import send_to_kafka
from app.config import Config


def process_notification(data, token):
    client_id = verify_api_token(token)
    if not client_id:
        return {"error": "Unauthorized", "status_code": 401}

    required_fields = ["recipient_id", "notification_type", "channel", "content"]
    if not all(field in data for field in required_fields):
        return {"error": "Missing required fields", "status_code": 400}

    try:
        resp = requests.get(
            f"{Config.USER_PREF_SERVICE_URL}/{data['recipient_id']}",
            params={"client_id": client_id}
        )
        if resp.status_code != 200:
            return {"error": "Failed to fetch user preferences", "status_code": 502}

        prefs = resp.json()
        if data["channel"] not in prefs.get("channels", []) or \
           data["notification_type"] not in prefs.get("allowed_types", []):
            return {"error": "User preference rejected", "status_code": 403}

    except Exception as e:
        return {"error": f"Preference service error: {str(e)}", "status_code": 500}

    message = {
        "client_id": client_id,
        "user_id": data["recipient_id"],
        "notification_type": data["notification_type"],
        "channel": data["channel"],
        "content": data["content"]
    }

    topic = f"{data['channel']}_notifications"
    send_to_kafka(topic, message)

    return {"message": "Notification accepted"}, 202
