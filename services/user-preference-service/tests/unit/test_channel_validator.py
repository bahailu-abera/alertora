import unittest
from app.validators.channel_validator import validate_channels


class TestValidateChannels(unittest.TestCase):
    def test_valid_channels(self):
        valid, error = validate_channels(["email", "sms"])
        self.assertTrue(valid)
        self.assertIsNone(error)

    def test_invalid_channel_type(self):
        valid, error = validate_channels("email")
        self.assertFalse(valid)
        self.assertEqual(error, "Channels must be a list.")

    def test_invalid_channel_value(self):
        valid, error = validate_channels(["email", "pigeon"])
        self.assertFalse(valid)
        self.assertIn("Invalid channels", error)


if __name__ == "__main__":
    unittest.main()
