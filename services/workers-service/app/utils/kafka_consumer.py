from kafka import KafkaConsumer
import json
import os


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


def consume_kafka_topic(topic, group_id, handler_func):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
    )

    for message in consumer:
        try:
            handler_func(message.value)
        except Exception as e:
            print(f"[ERROR] Failed to process message: {e}")
