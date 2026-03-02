# schemas/schema_loader.py

"""
A2A Schema Loader

Loads official A2A v1.0 schemas from vendored a2a-protocol.org spec.

The official schema should be downloaded and vendored at:
  schemas/official/a2a_v1.0_spec.json

Download from: https://a2a-protocol.org/latest/spec/a2a.json

Usage:
    from schemas.schema_loader import A2ASchemaLoader
    
    loader = A2ASchemaLoader()
    request_schema = loader.get_schema("request")
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional


class A2ASchemaLoader:
    """
    Loads and manages official A2A v1.0 schemas from a2a-protocol.org
    
    Source: https://a2a-protocol.org/latest/spec/a2a.json
    """
    
    # Update this when you update the vendored schema
    # Set to None to skip checksum verification
    EXPECTED_CHECKSUM = None
    
    def __init__(self, spec_path: Optional[Path] = None):
        if spec_path is None:
            spec_path = Path(__file__).parent / "official" / "a2a_v1.0_spec.json"
        
        self.spec_path = spec_path
        
        # Verify checksum if configured
        if self.EXPECTED_CHECKSUM:
            self._verify_checksum()
        
        # Load spec
        with open(spec_path) as f:
            self.spec = json.load(f)
        
        # Cache extracted schemas
        self._cache_schemas()
    
    def _verify_checksum(self):
        """Verify schema hasn't been tampered with or accidentally modified"""
        content = self.spec_path.read_bytes()
        actual = hashlib.sha256(content).hexdigest()
        
        if actual != self.EXPECTED_CHECKSUM:
            raise ValueError(
                f"A2A spec checksum mismatch!\n"
                f"Expected: {self.EXPECTED_CHECKSUM}\n"
                f"Got: {actual}\n"
                f"Either the schema was modified or you need to update EXPECTED_CHECKSUM"
            )
    
    def _cache_schemas(self):
        """Extract and cache individual schema definitions"""
        # The structure depends on the actual a2a.json format
        # Adjust based on what you find at https://a2a-protocol.org/latest/spec/a2a.json
        
        # Try common JSON Schema locations
        definitions = (
            self.spec.get("$defs", {}) or 
            self.spec.get("definitions", {}) or
            self.spec.get("components", {}).get("schemas", {})
        )
        
        self._schemas = {
            "request": self._find_schema(definitions, "Request"),
            "response": self._find_schema(definitions, "Response"),
            "error": self._find_schema(definitions, "Error"),
            "event": self._find_schema(definitions, "Event"),
        }
    
    def _find_schema(self, definitions: Dict, schema_name: str) -> Dict[str, Any]:
        """
        Find schema by name in definitions.
        Tries common naming variations.
        """
        # Try common variations
        variations = [
            schema_name,
            f"A2A{schema_name}",
            f"a2a_{schema_name.lower()}",
            schema_name.lower(),
            schema_name.upper(),
        ]
        
        for key in variations:
            if key in definitions:
                return definitions[key]
        
        raise KeyError(
            f"Schema '{schema_name}' not found in spec definitions. "
            f"Available schemas: {list(definitions.keys())}"
        )
    
    def get_schema(self, schema_type: str) -> Dict[str, Any]:
        """
        Get specific schema type.
        
        Args:
            schema_type: One of 'request', 'response', 'error', 'event'
        
        Returns:
            JSON schema dict
        """
        if schema_type not in self._schemas:
            raise ValueError(
                f"Unknown schema type: {schema_type}. "
                f"Valid types: {list(self._schemas.keys())}"
            )
        
        return self._schemas[schema_type]
    
    def get_all_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Get all cached schemas"""
        return self._schemas.copy()
    
    @property
    def version(self) -> str:
        """Get A2A spec version"""
        version_file = self.spec_path.parent / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        return "unknown"
