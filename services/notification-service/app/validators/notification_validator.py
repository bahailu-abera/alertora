from app.utils.constants import VALID_CHANNELS


def validate_notification_payload(data):
    """Ensure required fields are present in the notification payload."""
    required = {"recipient_id", "notification_type", "channel", "content"}
    if not data or not required.issubset(data.keys()):
        return False, "Missing required fields"

    return True, None


def validate_channel(channel):
    """Check if the channel is one of the accepted types."""
    return channel in VALID_CHANNELS
