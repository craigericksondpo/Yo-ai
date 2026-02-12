# lambda/data_steward/handler.py

from typing import Any, Dict
import json

from .runtime.envelope import build_envelope
from .runtime.context import build_context
from .router import dispatch_capability


def handler(event: Dict[str, Any], aws_context: Any) -> Dict[str, Any]:
    envelope = build_envelope(event, agent_type="data-steward")
    ctx = build_context(envelope)  # enforces profile + auth for data-steward

    result = dispatch_capability(ctx, envelope["raw_input"])

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result),
    }
