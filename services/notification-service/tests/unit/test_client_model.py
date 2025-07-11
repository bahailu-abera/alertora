import unittest
from app.models.client_model import ClientModel
from datetime import datetime


class TestClientModel(unittest.TestCase):
    def setUp(self):
        self.client_id = "1234"
        self.service_name = "TestApp"
        self.api_token = "securetoken"
        self.notification_types = [
            {"name": "promo", "description": "Promotions"},
            {"name": "alert", "description": "System alerts"},
        ]

    def test_to_dict(self):
        client = ClientModel(
            client_id=self.client_id,
            service_name=self.service_name,
            api_token=self.api_token,
            notification_types=self.notification_types,
        )
        data = client.to_dict()

        self.assertEqual(data["client_id"], self.client_id)
        self.assertEqual(data["service_name"], self.service_name)
        self.assertEqual(data["api_token"], self.api_token)
        self.assertEqual(data["notification_types"], self.notification_types)
        self.assertIsInstance(data["created_at"], datetime)

    def test_from_dict(self):
        input_data = {
            "client_id": self.client_id,
            "service_name": self.service_name,
            "api_token": self.api_token,
            "notification_types": self.notification_types,
        }
        client = ClientModel.from_dict(input_data)

        self.assertEqual(client.client_id, self.client_id)
        self.assertEqual(client.service_name, self.service_name)
        self.assertEqual(client.api_token, self.api_token)
        self.assertEqual(client.notification_types, self.notification_types)


if __name__ == "__main__":
    unittest.main()
