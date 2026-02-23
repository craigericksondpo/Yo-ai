# envelope.py - A2A envelopes, message wrappers
"""
Semantic envelope models for Yo-AI agents.

FastA2A handles transport envelopes.
This module defines the semantic AgentContext and Envelope models
that the Solicitor-General and agents use internally.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, List


@dataclass
class AgentContext:
    """
    Semantic context extracted from the incoming envelope.
    This is what agents actually consume.
    """
    caller: Optional[str]
    subject: Optional[str]
    profile: Optional[Dict[str, Any]]
    profile_patch: Optional[Dict[str, Any]]
    governance_labels: List[str]
    correlation_id: Optional[str]


@dataclass
class InputEnvelope:
    """
    Profile-aware input envelope passed to agent capabilities.
    """
    payload: Dict[str, Any]
    profile: Optional[Dict[str, Any]] = None
    profile_patch: Optional[Dict[str, Any]] = None
    governance_labels: Optional[List[str]] = None
    caller: Optional[str] = None
    subject: Optional[str] = None
    correlation_id: Optional[str] = None


@dataclass
class OutputEnvelope:
    """
    Profile-aware output envelope returned by agent capabilities.
    """
    result: Dict[str, Any]
    profile: Optional[Dict[str, Any]] = None
    profile_patch: Optional[Dict[str, Any]] = None
    governance_labels: Optional[List[str]] = None
    correlation_id: Optional[str] = None
