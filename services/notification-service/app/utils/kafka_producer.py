from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import time


_producer = None


def create_producer():
    retries = 5
    delay = 5
    for i in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            return producer
        except NoBrokersAvailable:
            if i == retries - 1:
                raise
            print(f"Kafka not ready, retrying in {delay} seconds...")
            time.sleep(delay)


def get_producer():
    global _producer
    if _producer is None:
        _producer = create_producer()
    return _producer


def send_to_kafka(topic, message):
    producer = get_producer()
    producer.send(topic, value=message)
    producer.flush()
