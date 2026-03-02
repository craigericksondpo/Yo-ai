# a2a/transport.py

from typing import Any
import uuid
from datetime import datetime
from .a2a_validator import A2AValidator

class A2ATransport:
    """Handles A2A v1.0 protocol envelope management"""
    
    def __init__(self, broker):
        self.broker = broker  # Your Solicitor-General
        self.validator = A2AValidator()
        self.pending_requests = {}  # Correlation tracking
    
    def handle_request(self, raw_request: dict) -> dict:
        """Public entry point - validates and routes"""
        # 1. Validate A2A envelope
        if not self._validate_envelope(raw_request):
            return self._error_response("Invalid A2A request", 400)
        
        # 2. Extract and correlate
        request_id = raw_request.get('id', str(uuid.uuid4()))
        self.pending_requests[request_id] = {
            'received_at': datetime.utcnow(),
            'original_request': raw_request
        }
        
        # 3. Hand to broker (unwrapped)
        try:
            result = self.broker.route_request(raw_request['params'])
            return self._success_response(result, request_id)
        except Exception as e:
            return self._error_response(str(e), request_id)
        finally:
            # Cleanup correlation
            self.pending_requests.pop(request_id, None)
    
    def handle_event(self, event: dict) -> None:
        """Handle A2A events (notifications)"""
        # Events don't need responses, but may need correlation
        pass
        
    def _validate_envelope(self, request: dict) -> bool:
        """Validate incoming A2A request"""
        return self.validator.validate_request(request)

    
    def _success_response(self, result: Any, request_id: str) -> dict:
        """Wrap in A2A v1.0 response envelope"""
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }
    
        if not self.validator.validate_response(response):
            return self._error_response(
                "Internal error: invalid response",
                request_id,
                -32603
            )
    
        return response

    
    def _error_response(self, message: str, request_id: str, code: int = -32603) -> dict:
        """A2A v1.0 error envelope"""
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": request_id
        }

        if not self.validator.validate_error(error):
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": "Internal error"},
                "id": request_id
            }
    
        return error
