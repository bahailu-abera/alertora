from app.utils.kafka_consumer import consume_kafka_topic
from app.services.email_service import retry_email_message


def run():
    consume_kafka_topic(
        topic="email_retries",
        group_id="email_retry_worker_group",
        handler_func=retry_email_message,
    )
