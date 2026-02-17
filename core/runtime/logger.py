"""
Simple, structured logger for Lambda and local dev.

Uses standard library logging but enforces consistent formatting.
"""

import json
import logging
import sys


def _configure_logger() -> logging.Logger:
    logger = logging.getLogger("yoai")
    if logger.handlers:
        return logger  # already configured

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONLogFormatter())

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


class JSONLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
        }
        return json.dumps(payload)


logger = _configure_logger()