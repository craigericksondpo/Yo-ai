# core/runtime/logging/log_bootstrapper.py

import time
import uuid
import socket
from typing import Optional, Dict

from .sink_loader import load_log_sink


class LogBootstrapper:
    """
    Initializes the platform logging sink and provides a uniform write() API.
    Each named instance is a singleton, tracked by the module-level registry.
    This does not use Python's logging module; it uses your existing sink model.
    """

    def __init__(self, name: str):
        self.name = name
        self.sink = load_log_sink()
        self.hostname = socket.gethostname()
        self.write({
            "event_type": "logger_initialized",
            "message": f"{name} logger started",
        })

    def _enrich(self, record: Dict) -> Dict:
        """
        Adds standard fields to every log record, including logger identity.
        """
        return {
            "timestamp": time.time(),
            "logger": self.name,
            "host": self.hostname,
            "sink_type": type(self.sink).__name__,
            "correlation_id": record.get("correlation_id", str(uuid.uuid4())),
            "level": record.get("level", "INFO"),
            "actor": record.get("actor", self.name),
            "event_type": record.get("event_type", "log"),
            "message": record.get("message", ""),
            "payload": record.get("payload", {}),
        }

    def write(self, record: Dict):
        """
        Enriches and writes a structured log record to the configured sink.
        """
        enriched = self._enrich(record)
        self.sink.write(enriched)


# Named singleton registry — one instance per logger name, per warm container
_registry: Dict[str, LogBootstrapper] = {}


def get_logger(name: str) -> LogBootstrapper:
    """
    Returns the singleton LogBootstrapper for the given name, creating it
    on first call. Subsequent calls with the same name return the cached instance.
    """
    global _registry
    if name not in _registry:
        _registry[name] = LogBootstrapper(name)
    return _registry[name]
