def validate_registration_payload(data):
    """Validate required fields for client registration."""
    if not data:
        return False, "No input provided"

    service_name = data.get("service_name")
    notification_types = data.get("notification_types")

    if not service_name:
        return False, "Missing service_name"

    if not isinstance(notification_types, list) or not all(
        isinstance(t, dict) and "name" in t and "description" in t for t in notification_types
    ):
        return False, "Invalid or missing notification_types"

    return True, None
