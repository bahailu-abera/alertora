import unittest
from unittest.mock import patch
from app.services.email_service import handle_email_message


class TestEmailWorker(unittest.TestCase):
    @patch("app.services.email_service.update_notification_status")
    @patch("app.services.email_service.send_email_via_gmail")
    @patch("app.services.email_service.log_notification_event")
    def test_handle_email_success(self, mock_log, mock_send, mock_update):
        mock_log.return_value = "log123"
        message = {
            "client_id": "cid",
            "user_id": "uid",
            "notification_type": "promo",
            "content": {"msg": "Hello"},
        }

        handle_email_message(message)

        mock_log.assert_called_once()
        mock_send.assert_called_once()
        mock_update.assert_called_with("log123", status="sent")

    @patch("app.services.email_service.update_notification_status")
    @patch(
        "app.services.email_service.send_email_via_gmail",
        side_effect=Exception("fail"),
    )
    @patch("app.services.email_service.log_notification_event")
    def test_handle_email_failure(self, mock_log, mock_send, mock_update):
        mock_log.return_value = "log456"
        message = {
            "client_id": "cid",
            "user_id": "uid",
            "notification_type": "promo",
            "content": {"msg": "Hello"},
        }

        handle_email_message(message)
        mock_update.assert_called_with(
            "log456", status="retry_pending", increment_retry=True
        )


if __name__ == "__main__":
    unittest.main()
