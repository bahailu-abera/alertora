from app.utils.kafka_consumer import consume_kafka_topic
from app.services.email_service import handle_email_message


def run():
    consume_kafka_topic(
        topic="email_notifications",
        group_id="email_worker_group",
        handler_func=handle_email_message,
    )
