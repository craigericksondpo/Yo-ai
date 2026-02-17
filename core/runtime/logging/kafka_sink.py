# core/runtime/logging/kafka_sink.py

import json
from kafka import KafkaProducer
from .log_sink import LogSink

class KafkaSink(LogSink):
    def __init__(self, brokers: str, topic: str):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=brokers.split(","),
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def write(self, record: dict):
        self.producer.send(self.topic, record)
        self.producer.flush()
