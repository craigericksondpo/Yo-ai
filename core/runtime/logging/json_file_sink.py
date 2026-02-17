# core/runtime/logging/json_file_sink.py

import json
from pathlib import Path
from .log_sink import LogSink

class JsonFileSink(LogSink):
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, record: dict):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
