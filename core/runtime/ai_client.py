# core/runtime/ai_client.py
#
# AI client for Yo-ai agents.
# Constructed by YoAiAgent at init from the agent's x-ai block (if present).
# Provides chat_completion(system, user, capability_id=None) consumed by call_ai().
#
# Model resolution order (env-first, per resolution design):
#   1. YO_AI_MODEL_<AGENT>_<SKILL>   e.g. YO_AI_MODEL_DOOR_KEEPER_TRUST_ASSIGN
#   2. YO_AI_MODEL_<AGENT>           e.g. YO_AI_MODEL_DOOR_KEEPER
#   3. x-ai.skills.<skill>.declared_defaults[role=primary]   (per-capability)
#   4. x-ai.declared_defaults[role=primary]                  (per-agent flat list)
#   5. Platform fallback: anthropic / claude-sonnet-4-6
#
# Graceful degradation — nothing crashes when x-ai is:
#   absent entirely          → platform fallback
#   present, no skills key   → per-agent declared_defaults or fallback
#   present, skill missing   → per-agent declared_defaults or fallback
#   declared_defaults empty  → fallback
#   declared_defaults has no "primary" role → first entry used
#   api_key_env / endpoint fields present (legacy) → silently ignored
#
# Per-agent vs per-capability:
#   Door-Keeper: x-ai.skills.<capability>.declared_defaults (per-capability)
#   All others:  x-ai.declared_defaults flat list (per-agent)
#   Both resolve transparently — per-capability tried first, per-agent fallback.
#
# api_key_env and endpoint:
#   Must NOT appear in publishable cards (API_KEYS.docx ruling).
#   Silently ignored if present in legacy cards.
#   API keys read from environment only:
#     ANTHROPIC_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, AZURE_OPENAI_KEY

import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

_FALLBACK_PROVIDER = "anthropic"
_FALLBACK_MODEL    = "claude-sonnet-4-6"


# ---------------------------------------------------------------------------
# AiClient
# ---------------------------------------------------------------------------

class AiClient:
    """
    AI client for a Yo-ai agent. Constructed once at agent init.

    Reads the agent's x-ai block (if present) for model preferences.
    All missing/partial configurations degrade to the platform fallback
    without raising.

    Usage in YoAiAgent.__init__():
        self.ai_client = AiClient(
            agent_name=self.name,
            xai_block=(self.extended or {}).get("x-ai"),
        )

    chat_completion() signature matches what call_ai() in ai_transform.py
    expects: chat_completion(system, user) → str
    capability_id is accepted as an optional kwarg for per-skill resolution.
    """

    def __init__(
        self,
        agent_name: str,
        xai_block: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.agent_name = agent_name
        # Normalise: always a dict internally, never None
        self._xai = xai_block if isinstance(xai_block, dict) else {}

        if not self._xai:
            logger.debug(
                "AiClient(%s): no x-ai block — platform fallback %s/%s.",
                agent_name, _FALLBACK_PROVIDER, _FALLBACK_MODEL
            )
        elif "skills" in self._xai:
            logger.debug(
                "AiClient(%s): per-capability x-ai (%d skill(s)).",
                agent_name, len(self._xai["skills"])
            )
        else:
            logger.debug("AiClient(%s): per-agent x-ai.", agent_name)

    # ------------------------------------------------------------------
    # Public interface — called by call_ai() in ai_transform.py
    # ------------------------------------------------------------------

    def chat_completion(
        self,
        system: str,
        user: str,
        capability_id: Optional[str] = None,
    ) -> str:
        """
        Resolve model, call provider, return raw text response.

        capability_id is optional — when supplied enables per-skill
        model selection (Door-Keeper pattern). When absent falls through
        to per-agent or platform fallback.

        Never raises. Returns an error JSON string on total failure so
        call_ai() can wrap it in {"rawText": ...} cleanly.
        """
        primary_provider, primary_model = self._resolve(capability_id, role="primary")

        logger.info(
            "AiClient(%s): %s/%s  capability=%s",
            self.agent_name, primary_provider, primary_model,
            capability_id or "none"
        )

        try:
            return _invoke(primary_provider, primary_model, system, user)
        except Exception as primary_exc:
            logger.warning(
                "AiClient(%s): primary %s/%s failed — %s. Trying failover.",
                self.agent_name, primary_provider, primary_model, primary_exc
            )

        # Try failover model from x-ai block
        failover_provider, failover_model = self._resolve(capability_id, role="failover")
        if (failover_provider, failover_model) != (primary_provider, primary_model):
            try:
                return _invoke(failover_provider, failover_model, system, user)
            except Exception as failover_exc:
                logger.error(
                    "AiClient(%s): failover %s/%s also failed — %s.",
                    self.agent_name, failover_provider, failover_model, failover_exc
                )

        # All providers exhausted
        return (
            f'{{"error": "AiClient({self.agent_name}): all providers failed '
            f'for capability {capability_id}"}}'
        )

    # ------------------------------------------------------------------
    # Model resolution
    # ------------------------------------------------------------------

    def _resolve(
        self,
        capability_id: Optional[str],
        role: str = "primary",
    ) -> Tuple[str, str]:
        """
        Resolve provider + model for a given role ("primary" or "failover").
        Works through the full resolution chain — never raises.
        Always returns a valid (provider, model) tuple.
        """
        # 1. Per-skill env override
        if capability_id:
            env_key = _env_key(self.agent_name, capability_id)
            if env_key in os.environ:
                return _parse_model_string(os.environ[env_key])

        # 2. Per-agent env override
        agent_env_key = _env_key(self.agent_name)
        if agent_env_key in os.environ:
            return _parse_model_string(os.environ[agent_env_key])

        # 3. x-ai per-capability (x-ai.skills.<capability>.declared_defaults)
        if capability_id and self._xai:
            skills = self._xai.get("skills")
            if isinstance(skills, dict):
                skill_cfg = skills.get(capability_id, {})
                result = _pick_from_defaults(
                    skill_cfg.get("declared_defaults", []), role
                )
                if result:
                    return result

        # 4. x-ai per-agent (x-ai.declared_defaults flat list)
        if self._xai:
            result = _pick_from_defaults(
                self._xai.get("declared_defaults", []), role
            )
            if result:
                return result

        # 5. Platform fallback
        return _FALLBACK_PROVIDER, _FALLBACK_MODEL


# ---------------------------------------------------------------------------
# Helpers — resolution
# ---------------------------------------------------------------------------

def _env_key(*parts: str) -> str:
    """Build a YO_AI_MODEL_... env var key from agent name and optional skill."""
    return "YO_AI_MODEL_" + "_".join(
        re.sub(r"[^A-Z0-9]", "_", p.upper()) for p in parts
    )


def _parse_model_string(value: str) -> Tuple[str, str]:
    """
    Parse "provider/model" env var value.
    "anthropic/claude-opus-4-6" → ("anthropic", "claude-opus-4-6")
    "claude-opus-4-6"           → (_FALLBACK_PROVIDER, "claude-opus-4-6")
    """
    if "/" in value:
        provider, model = value.split("/", 1)
        return provider.strip(), model.strip()
    return _FALLBACK_PROVIDER, value.strip()


def _pick_from_defaults(
    defaults: List[Dict[str, Any]],
    role: str,
) -> Optional[Tuple[str, str]]:
    """
    Pick a provider+model from a declared_defaults list by role.

    Graceful degradation:
      - defaults is None or not a list  → None
      - empty list                       → None
      - no entry with matching role      → first entry (any role)
      - entry missing provider or model  → skipped
      - api_key_env / endpoint present   → silently ignored
    """
    if not defaults or not isinstance(defaults, list):
        return None

    # Try exact role match first
    for entry in defaults:
        if not isinstance(entry, dict):
            continue
        if entry.get("role") == role:
            provider = entry.get("provider", "").strip()
            model    = entry.get("model", "").strip()
            if provider and model:
                # api_key_env and endpoint silently ignored here
                return provider, model

    # Fall back to first valid entry regardless of role
    for entry in defaults:
        if not isinstance(entry, dict):
            continue
        provider = entry.get("provider", "").strip()
        model    = entry.get("model", "").strip()
        if provider and model:
            return provider, model

    return None


# ---------------------------------------------------------------------------
# LLM invocation — one function per provider
# ---------------------------------------------------------------------------

def _invoke(provider: str, model: str, system: str, user: str) -> str:
    """Dispatch to the correct provider SDK. Raises on failure."""
    p = provider.lower().replace("-", "_")
    if p == "anthropic":
        return _call_anthropic(model, system, user)
    if p in ("google_gemini", "gemini"):
        return _call_gemini(model, system, user)
    if p == "openai":
        return _call_openai(model, system, user)
    if p in ("azure_openai", "azure"):
        return _call_azure(model, system, user)
    logger.warning(
        "AiClient: unknown provider '%s' — falling back to anthropic.", provider
    )
    return _call_anthropic(_FALLBACK_MODEL, system, user)


def _call_anthropic(model: str, system: str, user: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return msg.content[0].text


def _call_gemini(model: str, system: str, user: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    m = genai.GenerativeModel(model, system_instruction=system)
    return m.generate_content(user).text


def _call_openai(model: str, system: str, user: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.chat.completions.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    )
    return resp.choices[0].message.content


def _call_azure(model: str, system: str, user: str) -> str:
    from openai import AzureOpenAI
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_KEY"],
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        api_version="2024-02-01",
    )
    resp = client.chat.completions.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    )
    return resp.choices[0].message.content
