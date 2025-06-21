from app.utils.constants import VALID_CHANNELS


def validate_channels(channels):
    if not isinstance(channels, list):
        return False, "Channels must be a list."
    
    invalid = [ch for ch in channels if ch not in VALID_CHANNELS]
    if invalid:
        return False, f"Invalid channels: {invalid}"

    return True, None
