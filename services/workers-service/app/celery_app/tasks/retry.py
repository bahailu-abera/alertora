from app.celery_app import celery_app
from app.utils.postgress_utils import fetch_retry_pending_notifications, update_notification_status
from app.utils.email_provider import send_email_via_gmail
from app.utils.sms_provider import send_sms
from app.utils.push_provider import send_push_ios, send_push_android


import os


MAX_RETRIES = int(os.getenv("MAX_RETRIES", 5))


@celery_app.task(name="app.celery_app.tasks.retry.retry_failed_notifications")
def retry_failed_notifications():
    print("[INFO] Running unified retry task...")

    failed_logs = fetch_retry_pending_notifications(max_retries=MAX_RETRIES, limit=100)

    for log in failed_logs:
        print(f"[INFO] Retrying log ID: {log.id}, channel: {log.channel}, user: {log.user_id}")
        try:
            # Dispatch based on channel
            if log.channel == "email":
                send_email_via_gmail(log.user_id, log.content, log.user_id, log.client_id)
            elif log.channel == "sms":
                send_sms(log.user_id, log.content)
            elif log.channel == "push_ios":
                send_push_ios(log.user_id, log.content)
            elif log.channel == "push_android":
                send_push_android(log.user_id, log.content)
            else:
                raise ValueError(f"Unknown channel: {log.channel}")

            # Update as sent
            update_notification_status(log.id, status="sent", increment_retry=True)
            print(f"[SUCCESS] Log {log.id} marked as sent")
        except Exception as e:
            update_notification_status(log.id, status="retry_pending", increment_retry=True)
            print(f"[ERROR] Retry failed for log {log.id}: {e}")
