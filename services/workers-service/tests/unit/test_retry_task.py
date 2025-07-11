import unittest
from unittest.mock import patch, MagicMock
from app.celery_app.tasks.retry import retry_failed_notifications


class TestRetryTask(unittest.TestCase):
    @patch("app.celery_app.tasks.retry.fetch_retry_pending_notifications")
    @patch("app.celery_app.tasks.retry.send_email_via_gmail")
    @patch("app.celery_app.tasks.retry.update_notification_status")
    def test_retry_email_success(self, mock_update, mock_send, mock_fetch):
        log = MagicMock(
            id="log-id",
            channel="email",
            user_id="uid",
            client_id="cid",
            content={"msg": "test"},
        )
        mock_fetch.return_value = [log]

        retry_failed_notifications()

        mock_send.assert_called_once()
        mock_update.assert_called_with(
            "log-id", status="sent", increment_retry=True
        )

    @patch("app.celery_app.tasks.retry.fetch_retry_pending_notifications")
    @patch(
        "app.celery_app.tasks.retry.send_email_via_gmail",
        side_effect=Exception("fail"),
    )
    @patch("app.celery_app.tasks.retry.update_notification_status")
    def test_retry_email_failure(self, mock_update, mock_send, mock_fetch):
        log = MagicMock(
            id="log-id",
            channel="email",
            user_id="uid",
            client_id="cid",
            content={"msg": "test"},
        )
        mock_fetch.return_value = [log]

        retry_failed_notifications()

        mock_update.assert_called_with(
            "log-id", status="retry_pending", increment_retry=True
        )


if __name__ == "__main__":
    unittest.main()
