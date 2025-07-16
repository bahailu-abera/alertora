import unittest
from unittest.mock import patch
from app.services.preference_query_service import get_user_preference
import json


class TestPreferenceQueryService(unittest.TestCase):
    @patch("app.services.preference_query_service.get_cached_user_preference")
    def test_preference_from_cache(self, mock_cache):
        mock_cache.return_value = json.dumps(
            {"channels": ["email"], "allowed_types": ["promo"]}
        )

        resp, code = get_user_preference("user1", "client1")
        self.assertEqual(code, 200)
        self.assertIn("preferences", resp)
        self.assertEqual(resp["preferences"]["channels"], ["email"])

    @patch(
        "app.services.preference_query_service.get_cached_user_preference",
        return_value=None,
    )
    @patch(
        "app.services.preference_query_service.get_user_preference_document",
        return_value=None,
    )
    def test_no_preference_document(self, _, __):
        resp, code = get_user_preference("user1", "client1")
        self.assertEqual(code, 404)
        self.assertIn("No preferences found", resp["message"])

    @patch(
        "app.services.preference_query_service.get_cached_user_preference",
        return_value=None,
    )
    @patch(
        "app.services.preference_query_service.get_user_preference_document"
    )
    def test_no_preference_for_client(self, mock_get_doc, _):
        mock_get_doc.return_value = {"_id": "user1", "preferences": {}}
        resp, code = get_user_preference("user1", "client1")
        self.assertEqual(code, 404)
        self.assertIn("No preferences set", resp["message"])

    @patch(
        "app.services.preference_query_service.get_cached_user_preference",
        return_value=None,
    )
    @patch(
        "app.services.preference_query_service.get_user_preference_document"
    )
    @patch("app.services.preference_query_service.cache_user_preference")
    def test_preference_document_success(self, mock_cache, mock_get_doc, _):
        mock_get_doc.return_value = {
            "_id": "user1",
            "preferences": {
                "client1": {
                    "channels": ["push"],
                    "allowed_types": ["reminder"],
                }
            },
        }

        resp, code = get_user_preference("user1", "client1")
        self.assertEqual(code, 200)
        self.assertEqual(resp["preferences"]["channels"], ["push"])


if __name__ == "__main__":
    unittest.main()
