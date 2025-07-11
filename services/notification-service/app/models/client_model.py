from datetime import datetime


class ClientModel:
    def __init__(self, client_id, service_name, api_token, notification_types):
        self.client_id = client_id
        self.service_name = service_name
        self.api_token = api_token
        self.notification_types = notification_types
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "service_name": self.service_name,
            "api_token": self.api_token,
            "notification_types": self.notification_types,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return ClientModel(
            service_name=data.get("service_name"),
            api_token=data.get("api_token"),
            notification_types=data.get("notification_types", []),
            client_id=data.get("client_id"),
        )
