# core/runtime/load_fingerprints.py -- Compute stable fingerprints for agents based on their card and extended information.

import hashlib
import json
from typing import Dict, Any, List


def _stable_hash(value: Any) -> str:
    """
    Produce a deterministic SHA256 hash for any JSON-serializable value.
    Ensures stable ordering for lists/dicts.
    """
    normalized = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()



    # ------------------------------
    # Fingerprints
    # ------------------------------
    def _load_fingerprints(self) -> Dict[str, Any]:
        """
        Compute stable, deterministic fingerprints for the agent based on:
        - identity block
        - capabilities
        - tools
        - schemas
        - routing surface
        - full contract (agent card)
        """

        # Merge card + extended card (if present)
        merged_card = {}
        merged_card.update(self.card or {})
        if self.extended:
            merged_card.update(self.extended)

        # Extract surfaces
        identity_block = {
            "name": merged_card.get("name"),
            "version": merged_card.get("version"),
            "description": merged_card.get("description"),
            "domain": merged_card.get("domain"),
        }

        capabilities = sorted(merged_card.get("capabilities", []))
        tools = sorted(merged_card.get("tools", []))
        schemas = sorted(merged_card.get("schemas", []))
        routing = sorted(merged_card.get("routes", []))

        # Compute signatures
        identity_signature = _stable_hash(identity_block)
        capability_signature = _stable_hash(capabilities)
        tooling_signature = _stable_hash(tools)
        schema_signature = _stable_hash(schemas)
        routing_signature = _stable_hash(routing)

        # Full contract signature (the entire merged card)
        contract_signature = _stable_hash(merged_card)

        # Return structured fingerprint object
        return {
            "identity_signature": identity_signature,
            "capability_signature": capability_signature,
            "tooling_signature": tooling_signature,
            "schema_signature": schema_signature,
            "routing_signature": routing_signature,
            "contract_signature": contract_signature,
            "raw": {
                "identity": identity_block,
                "capabilities": capabilities,
                "tools": tools,
                "schemas": schemas,
                "routes": routing,
            },
        }