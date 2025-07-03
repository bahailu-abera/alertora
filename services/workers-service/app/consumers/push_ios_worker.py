from app.utils.kafka_consumer import consume_kafka_topic
from app.services.push_ios_service import handle_push_ios_message


def run():
    consume_kafka_topic(
        topic="push_ios_notifications",
        group_id="push_ios_worker_group",
        handler_func=handle_push_ios_message
    )
