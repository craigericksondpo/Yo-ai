# core/runtime/logging/log_sink.py

import abc

class LogSink(abc.ABC):
    """
    Abstract base class for all log sinks.
    """

    @abc.abstractmethod
    def write(self, record: dict):
        """
        Persist a structured log record.
        """
        raise NotImplementedError
