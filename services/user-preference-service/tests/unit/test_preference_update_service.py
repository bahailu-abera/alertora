import unittest
from unittest.mock import patch
from app.services.preference_update_service import update_user_preference


class TestPreferenceUpdateService(unittest.TestCase):
    @patch("app.services.preference_update_service.validate_channels")
    def test_invalid_channels(self, mock_validate):
        mock_validate.return_value = (False, "Invalid")
        resp, code = update_user_preference(
            "user1", "client1", "notalist", ["promo"]
        )
        self.assertEqual(code, 400)
        self.assertIn("error", resp)

    @patch(
        "app.services.preference_update_service.validate_channels",
        return_value=(True, None),
    )
    @patch(
        "app.services.preference_update_service."
        "update_user_preference_document"
    )
    @patch("app.services.preference_update_service.cache_user_preference")
    def test_successful_update(self, mock_cache, mock_update_doc, _):
        resp, code = update_user_preference(
            "user1", "client1", ["email"], ["promo"]
        )
        self.assertEqual(code, 200)
        self.assertEqual(resp["message"], "Preferences updated successfully.")


if __name__ == "__main__":
    unittest.main()
