import os
from app.extensions import SessionLocal
from app.models.notification_log_model import NotificationLog


def log_notification_event(log, session=None):
    """
    Logs a new notification event into the notification_logs table.
    """
    session = session or SessionLocal()
    try:
        session.add(log)
        session.commit()
        return log.id
    except Exception:
        session.rollback()
        raise
    finally:
        if session is None:
            session.close()


def update_notification_status(log_id, status, increment_retry=False, session=None):
    """
    Updates the status and optionally increments retry_count for a log entry.
    """
    session = session or SessionLocal()
    try:
        log = session.query(NotificationLog).filter(NotificationLog.id == log_id).first()
        if log:
            log.status = status
            if increment_retry:
                log.retry_count += 1
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        if session is None:
            session.close()


def fetch_retry_pending_notifications(max_retries=3, limit=100, session=None):
    """
    Fetch notifications that failed and are eligible for retry.
    """
    session = session or SessionLocal()
    try:
        return session.query(NotificationLog).filter(
            NotificationLog.status == "retry_pending",
            NotificationLog.retry_count < max_retries
        ).limit(limit).all()
    except Exception:
        raise
    finally:
        if session is None:
            session.close()
