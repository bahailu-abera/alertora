import os
from app.utils.jwt_utils import generate_preference_update_token


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
PREFERENCE_URL_BASE = os.getenv(
    "PREFERENCE_UPDATE_URL", "http://localhost/preferences"
)


def _append_preference_link(content: str, user_id: str, client_id: str) -> str:
    token = generate_preference_update_token(user_id, client_id)
    link = f"{PREFERENCE_URL_BASE}?token={token}"
    footer = f"\n\nTo manage your preferences, click here: {link}"
    return content + footer


def send_email_via_sendgrid(to_email, content, user_id=None, client_id=None):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    if not SENDGRID_API_KEY:
        raise Exception("SendGrid API Key not set")

    # Append link
    if user_id and client_id:
        content = _append_preference_link(content, user_id, client_id)

    message = Mail(
        from_email="noreply@alertora.com",
        to_emails=to_email,
        subject="Alertora Notification",
        plain_text_content=content,
    )

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)

    if response.status_code >= 400:
        raise ValueError(f"SendGrid error: {response.status_code}")


def send_email_via_gmail(
    to_email: str, content: str, user_id=None, client_id=None
):
    from email.message import EmailMessage
    import smtplib

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        raise ValueError("Gmail credentials not set")

    # Append link
    if user_id and client_id:
        content = _append_preference_link(content, user_id, client_id)

    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = "Alertora Notification"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Gmail error: {str(e)}")
        raise
