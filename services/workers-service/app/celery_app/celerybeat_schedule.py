import os
from datetime import timedelta
from celery.schedules import schedule


retry_interval_seconds = int(os.getenv("RETRY_INTERVAL_SECONDS", 60))


beat_schedule = {
    "retry-failed-notifications": {
        "task": "app.celery_app.tasks.retry.retry_failed_notifications",
        "schedule": schedule(run_every=timedelta(seconds=retry_interval_seconds)),
    }
}
