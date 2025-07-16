class UserPreference:
    def __init__(self, user_id, preferences=None):
        self.user_id = user_id
        self.preferences = preferences or {}

    def to_dict(self):
        return {"_id": self.user_id, "preferences": self.preferences}

    @staticmethod
    def from_dict(data):
        return UserPreference(
            user_id=data.get("_id"), preferences=data.get("preferences", {})
        )

    def update_preference(self, client_id, channels=None, allowed_types=None):
        if client_id not in self.preferences:
            self.preferences[client_id] = {}

        if channels is not None:
            self.preferences[client_id]["channels"] = channels
        if allowed_types is not None:
            self.preferences[client_id]["allowed_types"] = allowed_types
