from app.models.notification_log_model import NotificationLog
from app.utils.postgress_utils import log_notification_event


def handle_sms_message(message):
    print("[INFO] Processing SMS message:", message)

    success = True

    try:
        log = NotificationLog(
            client_id=message["client_id"],
            user_id=message["user_id"],
            notification_type=message["notification_type"],
            channel="sms",
            content=message["content"],
            status="sent" if success else "failed",
            retry_count=0,
        )
        log_notification_event(log)
    except Exception as e:
        print(f"[ERROR] Failed to log SMS notification: {e}")
