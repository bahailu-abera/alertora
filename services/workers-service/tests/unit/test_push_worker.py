import unittest
from unittest.mock import patch
from app.services.push_ios_service import handle_push_ios_message
from app.services.push_android_service import handle_push_android_message


class TestPushWorkers(unittest.TestCase):
    @patch("app.services.push_ios_service.log_notification_event")
    def test_handle_ios_success(self, mock_log):
        message = {
            "client_id": "cid",
            "user_id": "uid",
            "notification_type": "news",
            "content": {"msg": "Important"},
        }

        handle_push_ios_message(message)
        mock_log.assert_called_once()

    @patch("app.services.push_android_service.log_notification_event")
    def test_handle_android_success(self, mock_log):
        message = {
            "client_id": "cid",
            "user_id": "uid",
            "notification_type": "update",
            "content": {"msg": "Update now"},
        }

        handle_push_android_message(message)
        mock_log.assert_called_once()


if __name__ == "__main__":
    unittest.main()
