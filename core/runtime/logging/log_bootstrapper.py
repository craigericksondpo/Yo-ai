# core/runtime/logging/log_bootstrapper.py

import time
import uuid
import socket
from typing import Optional, Dict

from .sink_loader import load_log_sink


class LogBootstrapper:
    """
    Initializes the platform logging sink and provides a uniform write() API.
    This does not use Python's logging module; it uses your existing sink model.
    """

    def __init__(self):
        self.sink = load_log_sink()
        self.hostname = socket.gethostname()

    def _enrich(self, record: Dict) -> Dict:
        """
        Adds standard fields to every log record.
        """
        enriched = {
            "timestamp": time.time(),
            "host": self.hostname,
            "correlation_id": record.get("correlation_id", str(uuid.uuid4())),
            "level": record.get("level", "INFO"),
            "actor": record.get("actor", "unknown"),
            "event_type": record.get("event_type", "log"),
            "message": record.get("message", ""),
            "payload": record.get("payload", {}),
        }
        return enriched

    def write(self, record: Dict):
        """
        Writes a structured log record to the configured sink.
        """
        enriched = self._enrich(record)
        self.sink.write(enriched)


# Singleton instance used by all agents
_bootstrapper: Optional[LogBootstrapper] = None


def get_logger():
    """
    Returns the singleton LogBootstrapper instance.
    """
    global _bootstrapper
    if _bootstrapper is None:
        _bootstrapper = LogBootstrapper()
    return _bootstrapper
