# core/runtime/logging/s3_sink.py

import json
import uuid
import boto3
from .log_sink import LogSink

class S3Sink(LogSink):
    def __init__(self, bucket: str, prefix: str = "logs"):
        self.bucket = bucket
        self.prefix = prefix
        self.s3 = boto3.client("s3")

    def write(self, record: dict):
        key = f"{self.prefix}/{uuid.uuid4()}.json"
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=json.dumps(record)
        )
