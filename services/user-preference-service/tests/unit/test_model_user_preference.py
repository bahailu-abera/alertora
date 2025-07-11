import unittest
from app.models.preference_model import UserPreference


class TestUserPreferenceModel(unittest.TestCase):
    def test_to_dict_and_from_dict(self):
        model = UserPreference(
            "user123",
            {"client1": {"channels": ["email"], "allowed_types": ["promo"]}},
        )
        as_dict = model.to_dict()
        self.assertEqual(as_dict["_id"], "user123")
        self.assertIn("client1", as_dict["preferences"])

        recreated = UserPreference.from_dict(as_dict)
        self.assertEqual(recreated.user_id, "user123")
        self.assertEqual(
            recreated.preferences["client1"]["channels"], ["email"]
        )

    def test_update_preference(self):
        model = UserPreference("user456")
        model.update_preference(
            "clientX", channels=["sms"], allowed_types=["security"]
        )
        self.assertEqual(model.preferences["clientX"]["channels"], ["sms"])
        self.assertEqual(
            model.preferences["clientX"]["allowed_types"], ["security"]
        )


if __name__ == "__main__":
    unittest.main()
