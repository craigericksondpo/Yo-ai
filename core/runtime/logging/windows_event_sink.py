# core/runtime/logging/windows_event_sink.py

import json
import win32evtlogutil
from .log_sink import LogSink

class WindowsEventSink(LogSink):
    def __init__(self, source: str):
        self.source = source

    def write(self, record: dict):
        message = json.dumps(record)
        win32evtlogutil.ReportEvent(
            self.source,
            eventID=1,
            eventCategory=0,
            eventType=win32evtlogutil.EVENTLOG_INFORMATION_TYPE,
            strings=[message]
        )
