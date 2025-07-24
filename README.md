# Alertora

**Alertora** is a scalable, self-hostable notification delivery system for sending notifications via email, SMS, and push channels. It supports user preferences, asynchronous delivery, and multi-client registration.

## Features

- Client registration with custom notification types
- Send notifications via API
- Per-user notification preferences
- Asynchronous delivery using Celery workers
- Modular and extensible architecture

## Frontend

- Deployed Site: [https://alertora.addisalem.xyz](https://alertora.addisalem.xyz)
- Repository: [https://github.com/bahailu-abera/alertora-frontend](https://github.com/bahailu-abera/alertora-frontend)

## Deployment (Self-Hosting)

### Requirements

- Docker and Docker Compose
- SMTP credentials for sending emails
- (Optional) Domain name for production use

### Steps

1. Clone the repository
2. Create a `.env` file with required environment variables(see .env.example file)
3. Run `docker-compose up -d --build`

## API Usage

### Register a Client

#### Bash
```bash
curl -X POST https://api.alertora.addisalem.xyz/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "company_b",
    "notification_types": [
      {"name": "reminder", "description": "Reminders for tasks and events"},
      {"name": "feature_release", "description": "New feature announcements"},
      {"name": "promo", "description": "Sales and marketing messages"}
    ]
  }'
```

#### Python
```python
import requests

url = "https://api.alertora.addisalem.xyz/api/v1/register"
data = {
    "service_name": "company_b",
    "notification_types": [
        {"name": "reminder", "description": "Reminders for tasks and events"},
        {"name": "feature_release", "description": "New feature announcements"},
        {"name": "promo", "description": "Sales and marketing messages"}
    ]
}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=data, headers=headers)
print(response.json())
```

#### JavaScript
```javascript
fetch("https://api.alertora.addisalem.xyz/api/v1/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    service_name: "company_b",
    notification_types: [
      { name: "reminder", description: "Reminders for tasks and events" },
      { name: "feature_release", description: "New feature announcements" },
      { name: "promo", description: "Sales and marketing messages" }
    ]
  })
})
  .then(res => res.json())
  .then(console.log);
```

### Send a Notification

#### Bash
```bash
curl -X POST https://api.alertora.addisalem.xyz/api/v1/notify \
  -H "Authorization: Bearer <api_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_id": "hello@addisalem.com",
    "notification_type": "feature_release",
    "channel": "email",
    "content": "New feature: Dark mode is now available!"
  }'
```

#### Python
```python
import requests

url = "https://api.alertora.addisalem.xyz/api/v1/notify"
data = {
    "recipient_id": "hello@addisalem.com",
    "notification_type": "feature_release",
    "channel": "email",
    "content": "New feature: Dark mode is now available!"
}
headers = {
    "Authorization": "Bearer <api_token>",
    "Content-Type": "application/json"
}
response = requests.post(url, json=data, headers=headers)
print(response.json())
```

#### JavaScript
```javascript
fetch("https://api.alertora.addisalem.xyz/api/v1/notify", {
  method: "POST",
  headers: {
    "Authorization": "Bearer <api_token>",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    recipient_id: "hello@addisalem.com",
    notification_type: "feature_release",
    channel: "email",
    content: "New feature: Dark mode is now available!"
  })
})
  .then(res => res.json())
  .then(console.log);
```

## Features Under Development

- Third-party email provider integration (e.g., SendGrid, Mailgun)
- SMS and push notification channel support
- Admin dashboard for managing clients and notifications
