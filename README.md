#  Alertora Notification Delivery System

**Alertora** is a distributed, scalable notification delivery system that enables applications to send real-time alerts via **Email**, **SMS**, and **Push** channels. It respects user preferences and supports retries, delivery logging, and multi-channel queuing.

---

## 🧭 Project Overview

Alertora is designed to be:

- ✅ **Modular** — Each service handles a single responsibility.
- ⚙️ **Scalable** — Uses Kafka queues and stateless workers.
- 📬 **Flexible** — Pluggable provider support (SendGrid, Gmail, Twilio, FCM).
- 🔐 **Preference-Aware** — Users control which messages they receive.

---

## 🏗️ Architecture Overview

```
                         +--------------------------+
                         |      Client App          |
                         +--------------------------+
                                     |
                                     v
                            [ POST /notify ]
                                     |
                         +--------------------------+
                         | Notification Service     |
                         | - Auth & validation      |
                         | - User preference check  |                
                         | - Kafka enqueue          |
                         +--------------------------+
                                     |
                 +------------------------------------------+
                 |          Kafka Notification Topics       |
                 |    (email_notifications, sms_notifications)|
                 +------------------------------------------+
                        |                  |              |
                        v                  v              v
           +------------------+  +------------------+  +------------------+
           | Email Worker     |  | SMS Worker       |  | Push Worker      |
           | - SendGrid/Gmail |  | - Twilio         |  | - FCM/APNs       |
           +------------------+  +------------------+  +------------------+
                        |
                        v
              +----------------------+
              | PostgreSQL Logging   |
              +----------------------+
```

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
- `.env` file with:

```env
EMAIL_PROVIDER=gmail
GMAIL_ADDRESS=yourname@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

### ▶️ Start the System

```bash
docker-compose up --build
```

---

## 📦 Sending a Test Notification

```bash
# Register a client
curl -X POST http://localhost:5000/api/v1/register   -H "Content-Type: application/json"   -d '{"service_name": "MyApp", "notification_types": [
    {"name": "promo", "description": "Promotional offers"}
]}'

# Use the returned api_token to send a message
curl -X POST http://localhost:5000/api/v1/notify   -H "Authorization: Bearer <api_token>"   -H "Content-Type: application/json"   -d '{
    "recipient_id": "user@example.com",
    "notification_type": "promo",
    "channel": "email",
    "content": "This is a test email from Alertora"
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

