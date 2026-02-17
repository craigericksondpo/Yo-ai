# core/runtime/logging/dynamodb_sink.py

import boto3
from .log_sink import LogSink

class DynamoSink(LogSink):
    def __init__(self, table_name: str):
        self.table = boto3.resource("dynamodb").Table(table_name)

    def write(self, record: dict):
        self.table.put_item(Item=record)
