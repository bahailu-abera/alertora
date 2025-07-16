import unittest
from unittest.mock import patch
from app.services.registration_service import register_client


class TestRegistrationService(unittest.TestCase):
    @patch("app.services.registration_service.insert_client_document")
    @patch("app.services.registration_service.cache_auth_token")
    @patch("app.services.registration_service.validate_registration_payload")
    def test_register_client_success(
        self, mock_validate, mock_cache, mock_insert
    ):
        mock_validate.return_value = (True, None)
        mock_insert.return_value = None
        mock_cache.return_value = None

        client_data = {
            "service_name": "MyApp",
            "notification_types": [
                {"name": "promo", "description": "Promotional offers"},
                {
                    "name": "security_alert",
                    "description": "Security-related notifications",
                },
            ],
        }

        response = register_client(client_data)

        self.assertIn("client_id", response)
        self.assertIn("api_token", response)

    @patch("app.services.registration_service.validate_registration_payload")
    def test_register_client_invalid_payload(self, mock_validate):
        mock_validate.return_value = (False, "Missing required field")

        client_data = {
            "service_name": "MyApp"
            # Missing notification_types
        }

        response, status = register_client(client_data)

        self.assertEqual(status, 400)
        self.assertIn("error", response)
        self.assertEqual(response["error"], "Missing required field")


if __name__ == "__main__":
    unittest.main()
