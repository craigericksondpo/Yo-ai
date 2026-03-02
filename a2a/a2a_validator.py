# a2a/validator.py

"""
A2A v1.0 Validator

Validates A2A protocol messages against official schemas from:
https://a2a-protocol.org/latest/spec/a2a.json

Usage:
    from a2a_validator import A2AValidator
    
    validator = A2AValidator()
    
    if validator.validate_request(data):
        # Valid A2A request
    else:
        errors = validator.get_validation_errors(data, "request")
"""

from jsonschema import validate, ValidationError, Draft7Validator
from schemas.schema_loader import A2ASchemaLoader
from typing import Dict, Any, List


class A2AValidator:
    """
    Validates A2A v1.0 messages against official schemas from a2a-protocol.org
    """
    
    def __init__(self):
        # Load official schemas
        self.loader = A2ASchemaLoader()
        
        # Pre-compile validators for performance
        self._validators = {
            schema_type: Draft7Validator(schema)
            for schema_type, schema in self.loader.get_all_schemas().items()
        }
    
    def validate_request(self, data: Dict[str, Any]) -> bool:
        """
        Validate A2A request against official schema.
        
        Args:
            data: Request data to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self._validators["request"].validate(data)
            return True
        except ValidationError:
            return False
    
    def validate_response(self, data: Dict[str, Any]) -> bool:
        """
        Validate A2A response against official schema.
        
        Args:
            data: Response data to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self._validators["response"].validate(data)
            return True
        except ValidationError:
            return False
    
    def validate_error(self, data: Dict[str, Any]) -> bool:
        """
        Validate A2A error against official schema.
        
        Args:
            data: Error data to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self._validators["error"].validate(data)
            return True
        except ValidationError:
            return False
    
    def validate_event(self, data: Dict[str, Any]) -> bool:
        """
        Validate A2A event against official schema.
        
        Args:
            data: Event data to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            self._validators["event"].validate(data)
            return True
        except ValidationError:
            return False
    
    def get_validation_errors(self, data: Dict[str, Any], schema_type: str) -> List[Dict[str, Any]]:
        """
        Get detailed validation errors for debugging.
        
        Args:
            data: Data to validate
            schema_type: One of 'request', 'response', 'error', 'event'
            
        Returns:
            List of validation error details
        """
        errors = []
        validator = self._validators.get(schema_type)
        
        if not validator:
            return [{"error": f"Unknown schema type: {schema_type}"}]
        
        for error in validator.iter_errors(data):
            errors.append({
                "path": list(error.path),
                "message": error.message,
                "schema_path": list(error.schema_path),
                "validator": error.validator,
            })
        
        return errors
