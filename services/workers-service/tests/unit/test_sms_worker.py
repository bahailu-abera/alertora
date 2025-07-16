import unittest
from unittest.mock import patch
from app.services.sms_service import handle_sms_message


class TestSMSWorker(unittest.TestCase):
    @patch("app.services.sms_service.log_notification_event")
    def test_handle_sms_success(self, mock_log):
        message = {
            "client_id": "cid",
            "user_id": "uid",
            "notification_type": "otp",
            "content": {"text": "1234"},
        }

        handle_sms_message(message)
        mock_log.assert_called_once()


if __name__ == "__main__":
    unittest.main()
