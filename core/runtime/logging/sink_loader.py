# core/runtime/logging/sink_loader.py

import os

from .json_file_sink import JsonFileSink
from .s3_sink import S3Sink
from .dynamodb_sink import DynamoSink
from .windows_event_sink import WindowsEventSink
from .kafka_sink import KafkaSink

def load_log_sink():
    sink = os.getenv("LOG_SINK", "json").lower()

    if sink == "json":
        return JsonFileSink(os.getenv("LOG_PATH", "./logs/platform.jsonl"))

    if sink == "s3":
        return S3Sink(
            bucket=os.getenv("LOG_S3_BUCKET"),
            prefix=os.getenv("LOG_S3_PREFIX", "logs")
        )

    if sink == "dynamodb":
        return DynamoSink(os.getenv("LOG_DDB_TABLE"))

    if sink == "windows":
        return WindowsEventSink(os.getenv("WINDOWS_EVENT_SOURCE", "YoAIPlatform"))

    if sink == "kafka":
        return KafkaSink(
            brokers=os.getenv("KAFKA_BROKERS"),
            topic=os.getenv("KAFKA_TOPIC", "yoai-logs")
        )

    raise ValueError(f"Unknown LOG_SINK: {sink}")
