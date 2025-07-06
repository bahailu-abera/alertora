#  Alertora Notification Delivery System

**Alertora** is a distributed, scalable notification delivery system that enables applications to send real-time alerts via **Email**, **SMS**, and **Push** channels. It respects user preferences and supports retries, delivery logging, and multi-channel queuing.

---

🎥 **Project Demo:** [Watch the demo here](https://www.awesomescreenshot.com/video/41692293?key=24aa6ec597f55358125c85e7e8575927)  
🚀 **Deployed URL:** [https://api.alertora.addisalem.xyz](https://api.alertora.addisalem.xyz)

---

## 🧭 Project Overview

Alertora is designed to be:

- ✅ **Modular** — Each service handles a single responsibility.
- ⚙️ **Scalable** — Uses Kafka queues and stateless workers.
- 📬 **Flexible** — Pluggable provider support (SendGrid, Gmail, Twilio, FCM).
- 🔐 **Preference-Aware** — Users control which messages they receive.

---

## 🏗️ Architecture Overview (Data Flow)

1. Client sends request to `POST /notify` on the **Notification Service**.
2. Notification Service performs auth, validates request, checks preferences.
3. Message is published to the appropriate **Kafka topic** (email/sms/push).
4. A **Worker** consumes the message and sends it using the selected provider.
5. Result (success/failure) is logged in **PostgreSQL**.
6. Retries are handled by periodic **Celery tasks**.

---

## 🧩 Component Responsibilities

### 🔹 Notification Service (`services/notification-service`)
- Exposes:
  - `POST /register`: Register a new client.
  - `POST /notify`: Send a notification.
- Handles:
  - API token authentication
  - Request validation
  - User preference check
  - Enqueues messages to Kafka by channel

### 🔹 User Preference Service (`services/user-preference-service`)
- Exposes:
  - `GET /preferences`: Get user preferences
  - `POST /preferences`: Update user preferences
- Stores preferences in MongoDB
- Caches preferences in Redis

### 🔹 Worker Service (`services/workers-service`)
- Kafka consumers for each channel:
  - `email_worker`, `sms_worker`, `push_worker`
- Sends messages via pluggable providers:
  - Email: SendGrid or Gmail
  - SMS: Twilio
  - Push: FCM/APNs
- Logs delivery status to PostgreSQL
- Handles retries and status updates

---

## 🔐 Authentication

Clients authenticate using an `api_token` obtained during registration.  
Each request to `/notify` must include:

```
Authorization: Bearer <api_token>
```

---

## 🚀 API Documentation

### 1. `POST /register`

Register a new client application.

#### Request

```json
{
  "service_name": "MyApp",
  "notification_types": [
    {"name": "promo", "description": "Promotional offers"},
    {"name": "security_alert", "description": "Security-related notifications"}
  ]
}
```

#### Response

```json
{
  "client_id": "uuid-string",
  "api_token": "secure-token"
}
```

---

### 2. `POST /notify`

Send a notification.

#### Headers

```
Authorization: Bearer <api_token>
Content-Type: application/json
```

#### Request

```json
{
  "recipient_id": "user@example.com",
  "notification_type": "promo",
  "channel": "email",
  "content": "🔥 Big Sale starts now!"
}
```

#### Response

```json
{
  "message": "Notification accepted"
}
```

#### Error Cases

| Code | Message                             |
|------|-------------------------------------|
| 400  | Missing JSON body                   |
| 401  | Unauthorized                        |
| 403  | User preference rejected            |
| 502  | Failed to fetch user preferences    |

---

## 🛠️ Setup Instructions

### 📁 Prerequisites

- Docker & Docker Compose
- `.env` file with the following:

```env
BASE_URL=https://alertora.example.xyz

DOMAIN=api.alertora.example.xyz prefs.alertora.example.xyz
EMAIL=your_email@example.com
PREFERENCE_UPDATE_URL=https://prefs.alertora.example.xyz/preferences

GMAIL_ADDRESS=your_email_username

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# MongoDB
MONGO_URI=mongodb://mongodb:27017

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# JWT
JWT_SECRET_KEY=your_very_secret_jwt_key

# Email Providers
SENDGRID_API_KEY=your-sendgrid-api-key
MAIL_ADDRESS=your_email@example.com
GMAIL_APP_PASSWORD=your_gmail_app_password

# Celery Retry
MAX_RETRIES=5
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1
RETRY_INTERVAL_SECONDS=90

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=alertora
```

### ▶️ Start the System

```bash
docker-compose up --build
```

---

## 📦 Sending a Test Notification

```bash
# Register a client
curl -X POST https://api.alertora.example.xyz/api/v1/register   -H "Content-Type: application/json"   -d '{
        "service_name": "company_b",
       "notification_types": [
          {"name": "reminder", "description": "Reminders for tasks and events"},
          {"name": "feature_release", "description": "New feature announcements"},
          {"name": "promo", "description": "Sales and marketing messages"}
        ]
      }'

# Send notification
curl  -X POST https://api.alertora.example.xyz/api/v1/notify   -H "Authorization: Bearer <api_token>"   -H "Content-Type: application/json"   -d '{
        "recipient_id": "hello@example.com",
        "notification_type": "feature_release",
        "channel": "email",
        "content": "🚀 New feature: Dark mode is now available!"
      }'
```

---

## ⚙️ Folder Structure Overview

```
services/
├── notification-service       # API gateway
├── user-preference-service    # MongoDB + Redis for preferences
└── workers-service            # Kafka consumers + delivery logging
```

- Kafka topics separate concerns by channel
- PostgreSQL stores delivery logs
- MongoDB stores client & user settings

---
