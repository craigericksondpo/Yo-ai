from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Literal
from enum import Enum
import datetime as dt


# ---------- Supporting types ----------

class DecisionOutcome(str, Enum):
    APPROVE = "approve"
    DENY = "deny"
    ESCALATE = "escalate"
    REQUIRE_ADDITIONAL_INFO = "require_additional_info"


@dataclass
class DataRequest:
    """
    Represents a request to access or use personal data.
    """
    request_id: str
    requester_id: str               # calling agent / vendor / workflow
    purpose: str                    # e.g. "account_signup", "purchase", "identity_verification"
    purpose_category: str           # e.g. "core_service", "marketing", "fraud_prevention"
    requested_fields: List[str]     # e.g. ["email", "phone_number", "shipping_address"]
    channel: str                    # e.g. "webform", "phone", "email", "api"
    metadata: Dict[str, Any]        # arbitrary context (ip, user_agent, consent_ref, etc.)


@dataclass
class PolicyDecision:
    """
    The output of the policy engine evaluation.
    """
    outcome: DecisionOutcome
    allowed_fields: List[str]
    denied_fields: List[str]
    risk_score: float
    rationale: str
    policy_id: Optional[str] = None
    escalation_reason: Optional[str] = None


@dataclass
class MinimizedDataBundle:
    """
    The data bundle returned from the vault after minimization.
    """
    subject_id: str
    fields: Dict[str, Any]
    redacted_fields: List[str]


@dataclass
class SubjectProfile:
    """
    Simple in-memory representation matching the JSON schema below.
    """
    subject_id: str
    household_id: Optional[str]
    role: Literal["self", "spouse", "dependent", "caregiver", "household_admin"]
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    jurisdiction: str               # e.g. "US-CA"
    consent_prefs: Dict[str, Any]   # e.g. per-purpose consent settings
    risk_prefs: Dict[str, Any]      # e.g. max allowed risk per purpose category
    metadata: Dict[str, Any]


# ---------- Protocol interfaces ----------

class VaultAdapter(Protocol):
    """
    Interface for accessing subject-specific personal data vaults.
    Implementations may target Dropbox, S3, GDrive, etc.
    """

    def for_subject(self, subject_id: str) -> "VaultAdapter":
        ...

    async def fetch_fields(
        self,
        fields: List[str],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Fetch requested fields for the subject.
        Should NOT apply minimization logic; that’s policy’s job.
        """
        ...

    async def list_inventory(self) -> Dict[str, Any]:
        """
        Return a structured inventory of all known PI for this subject.
        """
        ...


class PolicyEngine(Protocol):
    """
    Interface for policy evaluation per subject.
    """

    def for_subject(self, subject_id: str) -> "PolicyEngine":
        ...

    async def evaluate_data_request(
        self,
        request: DataRequest,
        subject_profile: SubjectProfile,
    ) -> PolicyDecision:
        """
        Evaluate whether the request is allowed and which fields may be shared.
        """
        ...

    async def classify_risk(
        self,
        request: DataRequest,
        subject_profile: SubjectProfile,
    ) -> float:
        """
        Optional: compute a risk score for logging or UI.
        """
        ...


class AuditLogger(Protocol):
    """
    Interface for multi-tenant, per-subject audit logging.
    """

    def for_subject(self, subject_id: str) -> "AuditLogger":
        ...

    async def log_event(self, event: Dict[str, Any]) -> None:
        """
        Event should be immutable, append-only, schema-aligned.
        """
        ...


class WorkerAgentClient(Protocol):
    """
    Optional: used if DataSteward delegates to other workers
    (e.g., fraud-detector, PI-classifier, email-sender).
    """

    async def invoke(
        self,
        agent_id: str,
        skill: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        ...


# ---------- Core DataSteward class ----------

class DataSteward:
    """
    Multi-tenant Data-Steward.
    Each instance is bound to a single subject (person), but
    the class can be instantiated for any number of individuals.
    """

    def __init__(
        self,
        subject_profile: SubjectProfile,
        vault_adapter: VaultAdapter,
        policy_engine: PolicyEngine,
        audit_logger: AuditLogger,
        worker_client: Optional[WorkerAgentClient] = None,
    ) -> None:
        self.subject_profile = subject_profile
        self.subject_id = subject_profile.subject_id
        self.household_id = subject_profile.household_id

        # Scope each adapter to this subject
        self.vault = vault_adapter.for_subject(self.subject_id)
        self.policy = policy_engine.for_subject(self.subject_id)
        self.audit = audit_logger.for_subject(self.subject_id)
        self.workers = worker_client

    # ----- Core: Govern Data Requests -----

    async def govern_data_request(
        self,
        request: DataRequest,
    ) -> MinimizedDataBundle:
        """
        Evaluate intended use of personal data before granting access
        and return minimized data bundle if approved.
        """
        decision = await self.policy.evaluate_data_request(
            request=request,
            subject_profile=self.subject_profile,
        )

        event_base = {
            "event_type": "govern_data_request",
            "timestamp": dt.datetime.utcnow().isoformat() + "Z",
            "subject_id": self.subject_id,
            "household_id": self.household_id,
            "request_id": request.request_id,
            "requester_id": request.requester_id,
            "purpose": request.purpose,
            "purpose_category": request.purpose_category,
            "channel": request.channel,
        }

        if decision.outcome != DecisionOutcome.APPROVE:
            # Log denial / escalation / additional info
            await self.audit.log_event(
                {
                    **event_base,
                    "decision_outcome": decision.outcome.value,
                    "allowed_fields": decision.allowed_fields,
                    "denied_fields": decision.denied_fields,
                    "risk_score": decision.risk_score,
                    "rationale": decision.rationale,
                    "policy_id": decision.policy_id,
                    "escalation_reason": decision.escalation_reason,
                }
            )
            # Return an empty bundle or raise, depending on your contract
            return MinimizedDataBundle(
                subject_id=self.subject_id,
                fields={},
                redacted_fields=request.requested_fields,
            )

        # Fetch only allowed fields from the vault
        raw_data = await self.vault.fetch_fields(
            fields=decision.allowed_fields,
            context={
                "request_id": request.request_id,
                "purpose": request.purpose,
                "requester_id": request.requester_id,
            },
        )

        redacted_fields = [
            f for f in request.requested_fields if f not in decision.allowed_fields
        ]

        await self.audit.log_event(
            {
                **event_base,
                "decision_outcome": decision.outcome.value,
                "allowed_fields": decision.allowed_fields,
                "denied_fields": decision.denied_fields,
                "risk_score": decision.risk_score,
                "rationale": decision.rationale,
                "policy_id": decision.policy_id,
                "escalation_reason": decision.escalation_reason,
                "shared_fields": list(raw_data.keys()),
                "redacted_fields": redacted_fields,
            }
        )

        return MinimizedDataBundle(
            subject_id=self.subject_id,
            fields=raw_data,
            redacted_fields=redacted_fields,
        )

    # ----- Phone skills -----

    async def answer_phone(self, call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle inbound phone call:
        - verify caller
        - determine purpose
        - possibly trigger govern_data_request
        """
        timestamp = dt.datetime.utcnow().isoformat() + "Z"

        # Simple stub; you’ll later plug in a worker like 'caller-verifier'
        caller_id = call.get("caller_id")
        purpose = call.get("purpose", "unknown")

        await self.audit.log_event(
            {
                "event_type": "answer_phone",
                "timestamp": timestamp,
                "subject_id": self.subject_id,
                "household_id": self.household_id,
                "caller_id": caller_id,
                "call_metadata": call,
                "derived_purpose": purpose,
            }
        )

        # Return a structured response (for UI / another agent)
        return {
            "status": "received",
            "verified": False,  # placeholder
            "purpose": purpose,
        }

    async def call_phone(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make outbound call on behalf of the subject (verification, negotiation, rights requests).
        """
        timestamp = dt.datetime.utcnow().isoformat() + "Z"

        await self.audit.log_event(
            {
                "event_type": "call_phone",
                "timestamp": timestamp,
                "subject_id": self.subject_id,
                "household_id": self.household_id,
                "payload": payload,
            }
        )

        # Here you'd integrate with a telephony worker
        return {
            "status": "queued",
            "details": payload,
        }

    # ----- Email skills -----

    async def read_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process inbound email:
        - classify as spam / phishing / request / verification / etc.
        - extract possible workflows
        """
        timestamp = dt.datetime.utcnow().isoformat() + "Z"

        # Stub classification; later: call worker 'email-classifier'
        classification = "unknown"

        await self.audit.log_event(
            {
                "event_type": "read_email",
                "timestamp": timestamp,
                "subject_id": self.subject_id,
                "household_id": self.household_id,
                "classification": classification,
                "email_metadata": {
                    "from": email.get("from"),
                    "subject": email.get("subject"),
                    "headers": email.get("headers"),
                },
            }
        )

        return {
            "classification": classification,
            "recommended_action": "review",
        }

    async def send_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send outbound email as the subject's authorized agent.
        """
        timestamp = dt.datetime.utcnow().isoformat() + "Z"

        await self.audit.log_event(
            {
                "event_type": "send_email",
                "timestamp": timestamp,
                "subject_id": self.subject_id,
                "household_id": self.household_id,
                "email_metadata": {
                    "to": email.get("to"),
                    "subject": email.get("subject"),
                },
            }
        )

        # Here you'd integrate with an email-sender worker
        return {
            "status": "queued",
            "details": email,
        }
    
# from typing import TypedDict, List, Dict, Any, Optional
import datetime as dt


class OpportunityContext(TypedDict, total=False):
    """Context about an opportunity (rewards, purchase, talent)."""
    opportunity_id: str
    source_agent_id: str            # "rewards-seeker", "purchasing-agent", "talent-agent"
    category: str                   # "rewards", "shopping", "career"
    vendor_id: Optional[str]
    description: Optional[str]
    tags: List[str]                 # e.g. ["cashback", "job_application", "subscription"]
    metadata: Dict[str, Any]


class DataSteward:
    # ... same __init__ and other methods as before ...

    # ----- Worker collaboration: Rewards-Seeker -----

    async def prepare_rewards_profile(
        self,
        context: OpportunityContext,
    ) -> MinimizedDataBundle:
        """
        Provide a minimized rewards profile to Rewards-Seeker
        (e.g., preferences, loyalty IDs) without exposing full PI.
        """
        request = DataRequest(
            request_id=context.get("opportunity_id", "auto-" + dt.datetime.utcnow().isoformat()),
            requester_id=context.get("source_agent_id", "rewards-seeker"),
            purpose="rewards_matching",
            purpose_category="core_service",
            requested_fields=["loyalty_ids", "reward_preferences"],
            channel="agent_to_agent",
            metadata=context.get("metadata", {}),
        )

        return await self.govern_data_request(request)

    # ----- Worker collaboration: Purchasing-Agent -----

    async def prepare_purchase_bundle(
        self,
        context: OpportunityContext,
    ) -> MinimizedDataBundle:
        """
        Provide Purchasing-Agent with the minimum necessary data
        to complete a purchase (e.g., shipping address, email).
        """
        request = DataRequest(
            request_id=context.get("opportunity_id", "auto-" + dt.datetime.utcnow().isoformat()),
            requester_id=context.get("source_agent_id", "purchasing-agent"),
            purpose="purchase_checkout",
            purpose_category="core_service",
            requested_fields=["shipping_address", "billing_address", "email", "phone_number"],
            channel="agent_to_agent",
            metadata=context.get("metadata", {}),
        )

        return await self.govern_data_request(request)

    # ----- Worker collaboration: Talent-Agent -----

    async def prepare_talent_profile(
        self,
        context: OpportunityContext,
    ) -> MinimizedDataBundle:
        """
        Provide Talent-Agent with a minimized talent profile
        (e.g., resume data, skills) appropriate for a given opportunity.
        """
        request = DataRequest(
            request_id=context.get("opportunity_id", "auto-" + dt.datetime.utcnow().isoformat()),
            requester_id=context.get("source_agent_id", "talent-agent"),
            purpose="talent_opportunity",
            purpose_category="career",
            requested_fields=["resume", "skills_profile", "public_profile_links", "contact_email"],
            channel="agent_to_agent",
            metadata=context.get("metadata", {}),
        )

        return await self.govern_data_request(request)

# Result:
# •	Workers call these methods instead of touching the vault
# •	Data Steward runs policy + minimization + audit for each collaboration
# •	The same govern_data_request path is used for risk and opportunity flows

