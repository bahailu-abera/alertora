from app.utils.kafka_consumer import consume_kafka_topic
from app.services.push_android_service import handle_push_android_message


def run():
    consume_kafka_topic(
        topic="push_android_notifications",
        group_id="push_android_worker_group",
        handler_func=handle_push_android_message
    )
