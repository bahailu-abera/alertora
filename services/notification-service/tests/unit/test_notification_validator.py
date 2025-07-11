import unittest
from app.validators.notification_validator import (
    validate_notification_payload,
    validate_channel,
)
from app.validators.registration_validator import (
    validate_registration_payload,
)


class TestNotificationPayloadValidator(unittest.TestCase):
    def test_valid_payload(self):
        data = {
            "recipient_id": "user@example.com",
            "notification_type": "promo",
            "channel": "email",
            "content": "Hello world!",
        }
        valid, error = validate_notification_payload(data)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_missing_fields(self):
        data = {
            "recipient_id": "user@example.com",
            "channel": "email",
        }
        valid, error = validate_notification_payload(data)
        self.assertFalse(valid)
        self.assertEqual(error, "Missing required fields")


class TestChannelValidator(unittest.TestCase):
    def test_valid_channel(self):
        self.assertTrue(validate_channel("email"))
        self.assertTrue(validate_channel("sms"))

    def test_invalid_channel(self):
        self.assertFalse(validate_channel("pigeon"))


class TestRegistrationPayloadValidator(unittest.TestCase):
    def test_valid_registration(self):
        data = {
            "service_name": "MyService",
            "notification_types": [
                {"name": "promo", "description": "Promotions"},
                {"name": "security", "description": "Security alerts"},
            ],
        }
        valid, error = validate_registration_payload(data)
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_missing_service_name(self):
        data = {
            "notification_types": [
                {"name": "promo", "description": "Promotions"}
            ]
        }
        valid, error = validate_registration_payload(data)
        self.assertFalse(valid)
        self.assertEqual(error, "Missing service_name")

    def test_invalid_notification_types(self):
        data = {
            "service_name": "MyApp",
            "notification_types": ["just-a-string"],
        }
        valid, error = validate_registration_payload(data)
        self.assertFalse(valid)
        self.assertEqual(error, "Invalid or missing notification_types")


if __name__ == "__main__":
    unittest.main()
