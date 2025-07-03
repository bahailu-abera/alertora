from app.models.notification_log_model import NotificationLog
from app.utils.postgress_utils import log_notification_event


def handle_push_android_message(message):
    print("[INFO] Processing Android push message:", message)

    success = True 

    try:
        log = NotificationLog(
            client_id=message["client_id"],
            user_id=message["user_id"],
            notification_type=message["notification_type"],
            channel="push_android",
            content=message["content"],
            status="sent" if success else "failed",
            retry_count=0
        )
        log_notification_event(log)
    except Exception as e:
        print(f"[ERROR] Failed to log Android push notification: {e}")
