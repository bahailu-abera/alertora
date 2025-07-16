from app.utils.postgress_utils import (
    log_notification_event,
    update_notification_status,
)
from app.models.notification_log_model import NotificationLog
from app.utils.email_provider import send_email_via_gmail


def handle_email_message(message):
    print("[INFO] Received email message:", message)

    log = NotificationLog(
        client_id=message["client_id"],
        user_id=message["user_id"],
        notification_type=message["notification_type"],
        channel="email",
        content=message["content"],
        status="pending",
        retry_count=0,
    )

    log_id = log_notification_event(log)

    try:
        send_email_via_gmail(
            message["user_id"],
            message["content"],
            message["user_id"],
            message["client_id"],
        )
        update_notification_status(log_id, status="sent")
    except Exception as e:
        print(f"[ERROR] SendGrid failed: {e}")
        update_notification_status(
            log_id, status="retry_pending", increment_retry=True
        )
