import unittest
from unittest.mock import patch
from app.utils.email_provider import _append_preference_link


class TestEmailProvider(unittest.TestCase):
    @patch("app.utils.email_provider.generate_preference_update_token")
    def test_append_preference_link(self, mock_generate_token):
        mock_generate_token.return_value = "mockedtoken"
        content = "This is the message"
        user_id = "uid"
        client_id = "cid"

        result = _append_preference_link(content, user_id, client_id)

        self.assertIn("mockedtoken", result)
        self.assertIn("To manage your preferences", result)


if __name__ == "__main__":
    unittest.main()
