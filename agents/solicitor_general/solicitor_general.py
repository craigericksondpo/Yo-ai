# agents/solicitor_general/solicitor_general.py

"""
Solicitor-General: Root governance agent for the Yo-AI Platform.

Responsibilities:
  - Broker all A2A interactions
  - Enforce call-graph rules and trust tiers
  - Maintain correlation maps and routing continuity
  - Manage task lifecycle and dispatch
  - Log events and maintain platform auditability

PlatformAgents do NOT use profiles — they do not represent people.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

from core.platform_agent import PlatformAgent
from core.envelope import AgentContext


class TrustTier(Enum):
    """Trust tiers for agent-to-agent communication"""
    PLATFORM = "platform"      # Core platform agents (Solicitor-General, etc.)
    VERIFIED = "verified"      # Verified third-party agents
    SANDBOX = "sandbox"        # Untrusted/testing agents


class CallGraphRule:
    """Represents a call-graph authorization rule"""
    
    def __init__(self, caller: str, callee: str, capability: str, 
                 trust_tier: TrustTier, allowed: bool = True):
        self.caller = caller
        self.callee = callee
        self.capability = capability
        self.trust_tier = trust_tier
        self.allowed = allowed


class SolicitorGeneralAgent(PlatformAgent):
    """
    Root governance agent that brokers all A2A interactions.
    Implements the broker interface expected by A2ATransport.
    """

    def __init__(self, *, card, extended_card=None, context=None):
        super().__init__(
            card=card,
            extended_card=extended_card,
            context=context,
        )
        
        # Initialize governance structures
        self.call_graph_rules: List[CallGraphRule] = []
        self.agent_registry: Dict[str, Dict[str, Any]] = {}
        self.correlation_map: Dict[str, Dict[str, Any]] = {}
        self.event_log: List[Dict[str, Any]] = []
        
        # Initialize default platform rules
        self._initialize_default_rules()

    # ------------------------------------------------------------------
    # A2A Broker Interface (called by A2ATransport)
    # ------------------------------------------------------------------
    
    def route_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main routing method called by A2ATransport.
        Validates, authorizes, and dispatches A2A requests.
        
        Args:
            params: Unwrapped A2A request parameters
            
        Returns:
            Result dictionary to be wrapped by transport layer
        """
        # Extract routing information
        caller = params.get("caller")
        callee = params.get("callee")
        capability = params.get("capability")
        correlation_id = params.get("correlationId", str(uuid.uuid4()))
        
        # Log the request
        self._log_request(caller, callee, capability, correlation_id, params)
        
        # Validate request
        self._validate_routing_request(caller, callee, capability)
        
        # Check authorization
        if not self._authorize_call(caller, callee, capability):
            raise PermissionError(
                f"Agent {caller} not authorized to call {capability} on {callee}"
            )
        
        # Update correlation map
        self._track_correlation(correlation_id, caller, callee, capability, params)
        
        # Route to appropriate handler
        if callee == self.card.get("agentId"):
            # Request for Solicitor-General itself
            return self._handle_internal_capability(capability, params, correlation_id)
        else:
            # Request for another agent - dispatch
            return self._dispatch_to_agent(callee, capability, params, correlation_id)

    # ------------------------------------------------------------------
    # Internal Capabilities (Solicitor-General's own capabilities)
    # ------------------------------------------------------------------
    
    async def just_ask(self, envelope):
        """Handle general queries about platform governance"""
        from .just_ask import run
        return await run(envelope, self._build_context(envelope))

    async def event_log(self, envelope):
        """Retrieve governance event logs"""
        from .event_log import run
        return await run(envelope, self._build_context(envelope))
    
    async def authorize_call(self, envelope):
        """Check if a specific A2A call is authorized"""
        from core.runtime.authorize_call import run
        return await run(envelope, self._build_context(envelope))

    # ------------------------------------------------------------------
    # Governance & Authorization
    # ------------------------------------------------------------------
    
    def _initialize_default_rules(self):
        """Set up default call-graph rules for platform agents"""
        # Platform agents can call each other
        self.call_graph_rules.append(
            CallGraphRule("*", "*", "*", TrustTier.PLATFORM, allowed=True)
        )
        
        # Register self
        self.agent_registry[self.card.get("agentId", "solicitor-general")] = {
            "trust_tier": TrustTier.PLATFORM,
            "capabilities": ["JustAsk", "EventLog", "RegisterAgent", "AuthorizeCall"],
            "registered_at": datetime.utcnow().isoformat()
        }
    
    def _validate_routing_request(self, caller: str, callee: str, capability: str):
        """Validate that routing request has required fields"""
        if not caller:
            raise ValueError("Caller agent ID is required")
        if not callee:
            raise ValueError("Callee agent ID is required")
        if not capability:
            raise ValueError("Capability name is required")
    
    def _authorize_call(self, caller: str, callee: str, capability: str) -> bool:
        """
        Check if caller is authorized to invoke capability on callee.
        Implements call-graph rule enforcement.
        """
        # Get trust tiers
        caller_info = self.agent_registry.get(caller, {})
        callee_info = self.agent_registry.get(callee, {})
        
        caller_tier = caller_info.get("trust_tier", TrustTier.SANDBOX)
        callee_tier = callee_info.get("trust_tier", TrustTier.SANDBOX)
        
        # Check explicit rules first
        for rule in self.call_graph_rules:
            if self._rule_matches(rule, caller, callee, capability):
                return rule.allowed
        
        # Default policy: platform agents can call anything,
        # verified agents can call verified/sandbox,
        # sandbox agents can only call sandbox
        if caller_tier == TrustTier.PLATFORM:
            return True
        elif caller_tier == TrustTier.VERIFIED:
            return callee_tier in [TrustTier.VERIFIED, TrustTier.SANDBOX]
        else:  # SANDBOX
            return callee_tier == TrustTier.SANDBOX
    
    def _rule_matches(self, rule: CallGraphRule, caller: str, 
                      callee: str, capability: str) -> bool:
        """Check if a rule matches the given call"""
        return (
            (rule.caller == "*" or rule.caller == caller) and
            (rule.callee == "*" or rule.callee == callee) and
            (rule.capability == "*" or rule.capability == capability)
        )

    # ------------------------------------------------------------------
    # Correlation & Tracking
    # ------------------------------------------------------------------
    
    def _track_correlation(self, correlation_id: str, caller: str, 
                          callee: str, capability: str, params: Dict[str, Any]):
        """Maintain correlation map for request/response tracking"""
        self.correlation_map[correlation_id] = {
            "caller": caller,
            "callee": callee,
            "capability": capability,
            "started_at": datetime.utcnow().isoformat(),
            "status": "in_progress",
            "params": params
        }
    
    def _update_correlation(self, correlation_id: str, status: str, 
                           result: Optional[Dict[str, Any]] = None):
        """Update correlation tracking with result"""
        if correlation_id in self.correlation_map:
            self.correlation_map[correlation_id].update({
                "status": status,
                "completed_at": datetime.utcnow().isoformat(),
                "result": result
            })

    # ------------------------------------------------------------------
    # Dispatching & Routing
    # ------------------------------------------------------------------
    
    def _handle_internal_capability(self, capability: str, 
                                    params: Dict[str, Any], 
                                    correlation_id: str) -> Dict[str, Any]:
        """Handle requests directed at Solicitor-General itself"""
        # Map capability names to methods
        capability_map = {
            "JustAsk": self.just_ask,
            "EventLog": self.event_log,
            "RegisterAgent": self.register_agent,
            "AuthorizeCall": self.authorize_call,
        }
        
        handler = capability_map.get(capability)
        if not handler:
            raise ValueError(f"Unknown Solicitor-General capability: {capability}")
        
        # Build envelope for internal processing
        envelope = {
            "caller": params.get("caller"),
            "subject": params.get("subject"),
            "correlationId": correlation_id,
            "governanceLabels": params.get("governanceLabels", []),
            "payload": params.get("payload", {})
        }
        
        # Execute (may be async)
        import asyncio
        if asyncio.iscoroutinefunction(handler):
            result = asyncio.run(handler(envelope))
        else:
            result = handler(envelope)
        
        # Update correlation
        self._update_correlation(correlation_id, "completed", result)
        
        return result
    
    def _dispatch_to_agent(self, callee: str, capability: str, 
                          params: Dict[str, Any], 
                          correlation_id: str) -> Dict[str, Any]:
        """
        Dispatch request to another agent.
        This would integrate with your agent invocation system.
        """
        # TODO: Implement actual agent invocation
        # This could use Lambda, HTTP, or your platform's native transport
        
        # For now, return a placeholder
        result = {
            "status": "dispatched",
            "callee": callee,
            "capability": capability,
            "correlationId": correlation_id,
            "message": f"Request dispatched to {callee}.{capability}"
        }
        
        self._update_correlation(correlation_id, "dispatched", result)
        return result

    # ------------------------------------------------------------------
    # Logging & Auditability
    # ------------------------------------------------------------------
    
    def _log_request(self, caller: str, callee: str, capability: str, 
                    correlation_id: str, params: Dict[str, Any]):
        """Log A2A request for audit trail"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "a2a_request",
            "correlation_id": correlation_id,
            "caller": caller,
            "callee": callee,
            "capability": capability,
            "params": params,
        }
        self.event_log.append(event)
        
        # TODO: Persist to durable storage (DynamoDB, etc.)
    
    def _log_response(self, correlation_id: str, status: str, result: Any):
        """Log A2A response for audit trail"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "a2a_response",
            "correlation_id": correlation_id,
            "status": status,
            "result": result,
        }
        self.event_log.append(event)
        
        # TODO: Persist to durable storage

    # ------------------------------------------------------------------
    # Context builder (PlatformAgents do NOT use profiles)
    # ------------------------------------------------------------------
    
    def _build_context(self, envelope_dict: Dict[str, Any]) -> AgentContext:
        """Build agent context from envelope"""
        return AgentContext(
            caller=envelope_dict.get("caller"),
            subject=envelope_dict.get("subject"),
            profile=None,  # PlatformAgents don't use profiles
            profile_patch=None,
            governance_labels=envelope_dict.get("governanceLabels", []),
            correlation_id=envelope_dict.get("correlationId"),
        )
