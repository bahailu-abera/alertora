from app.utils.kafka_consumer import consume_kafka_topic
from app.services.sms_service import handle_sms_message


def run():
    consume_kafka_topic(
        topic="sms_notifications",
        group_id="sms_worker_group",
        handler_func=handle_sms_message
    )
