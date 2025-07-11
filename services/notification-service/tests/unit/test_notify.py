import unittest
from unittest.mock import patch, MagicMock
from app.services.notification_service import process_notification


class TestProcessNotification(unittest.TestCase):
    def setUp(self):
        self.valid_token = "valid_token"
        self.valid_client_id = "client_123"
        self.valid_data = {
            "recipient_id": "user@example.com",
            "notification_type": "promo",
            "channel": "email",
            "content": "Hello World!",
        }

    @patch("app.services.notification_service.send_to_kafka")
    @patch("app.services.notification_service.requests.get")
    @patch("app.services.notification_service.validate_notification_payload")
    @patch("app.services.notification_service.verify_api_token")
    def test_successful_notification(
        self, mock_verify, mock_validate, mock_requests_get, mock_send_kafka
    ):
        mock_verify.return_value = self.valid_client_id
        mock_validate.return_value = (True, None)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "preferences": {"channels": ["email"], "allowed_types": ["promo"]}
        }
        mock_requests_get.return_value = mock_response

        mock_send_kafka.return_value = None

        response, code = process_notification(
            self.valid_data, self.valid_token
        )
        self.assertEqual(code, 202)
        self.assertEqual(response["message"], "Notification accepted")

    @patch("app.services.notification_service.verify_api_token")
    def test_invalid_token(self, mock_verify):
        mock_verify.return_value = None

        response, code = process_notification(self.valid_data, "invalid_token")
        self.assertEqual(code, 401)
        self.assertEqual(response["error"], "Unauthorized")

    @patch("app.services.notification_service.validate_notification_payload")
    @patch("app.services.notification_service.verify_api_token")
    def test_invalid_payload(self, mock_verify, mock_validate):
        mock_verify.return_value = self.valid_client_id
        mock_validate.return_value = (False, "Invalid payload")

        response, code = process_notification({}, self.valid_token)
        self.assertEqual(code, 400)
        self.assertIn("error", response)

    @patch("app.services.notification_service.requests.get")
    @patch("app.services.notification_service.validate_notification_payload")
    @patch("app.services.notification_service.verify_api_token")
    def test_preference_service_failure(
        self, mock_verify, mock_validate, mock_requests_get
    ):
        mock_verify.return_value = self.valid_client_id
        mock_validate.return_value = (True, None)

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response

        response, code = process_notification(
            self.valid_data, self.valid_token
        )
        self.assertEqual(code, 502)
        self.assertIn("error", response)

    @patch("app.services.notification_service.requests.get")
    @patch("app.services.notification_service.validate_notification_payload")
    @patch("app.services.notification_service.verify_api_token")
    def test_user_preference_rejected(
        self, mock_verify, mock_validate, mock_requests_get
    ):
        mock_verify.return_value = self.valid_client_id
        mock_validate.return_value = (True, None)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "preferences": {
                "channels": ["sms"],  # mismatch
                "allowed_types": ["security"],  # mismatch
            }
        }
        mock_requests_get.return_value = mock_response

        response, code = process_notification(
            self.valid_data, self.valid_token
        )
        self.assertEqual(code, 403)
        self.assertEqual(response["error"], "User preference rejected")

    @patch("app.services.notification_service.requests.get")
    @patch("app.services.notification_service.validate_notification_payload")
    @patch("app.services.notification_service.verify_api_token")
    def test_exception_during_preference_request(
        self, mock_verify, mock_validate, mock_requests_get
    ):
        mock_verify.return_value = self.valid_client_id
        mock_validate.return_value = (True, None)
        mock_requests_get.side_effect = Exception("Connection timeout")

        response, code = process_notification(
            self.valid_data, self.valid_token
        )
        self.assertEqual(code, 500)
        self.assertIn("Preference service error", response["error"])


if __name__ == "__main__":
    unittest.main()
