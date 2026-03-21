# core/runtime/load_knowledge.py
#
# Load agent-specific and shared knowledge at agent initialization.
# Called by YoAiAgent.__init__() when slim=False.
#
# Changes from original:
#   - agent.card['name'] hard bracket → agent.card.get('name', agent.actor_name)
#     Gap Registry fix (✅🔧 fixed locally — now applied here)
#   - tree-files.txt preference removed: previously if tree-files.txt existed,
#     real files were skipped entirely. Now real files are always loaded;
#     tree-files.txt is loaded alongside them as an index artifact, not a
#     replacement. knowledge_query() needs real content to score relevance.
#   - .meta sidecar files excluded from knowledge load (provenance only)
#   - .docx support added via pandoc subprocess (consistent with knowledge_query)
#   - SHARED_ROOT and AGENTS_ROOT respect env overrides
#   - Errors per-file are logged, not silently swallowed
#
# Relationship to knowledge_query.py:
#   load_knowledge() = load ALL knowledge at init (bulk, for agent context)
#   knowledge_query() = retrieve RELEVANT fragments per-request (targeted)
#   Both read the same directories. Neither replaces the other.

import logging
import os
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Root paths — override via environment for Lambda/container deployments
_SHARED_ROOT = Path(os.environ.get("YO_AI_SHARED_ROOT", "shared")) / "knowledge"
_AGENTS_ROOT = Path(os.environ.get("YO_AI_AGENTS_ROOT", "agents"))

# File suffixes to exclude from knowledge load
_EXCLUDED_SUFFIXES = {".meta"}

# File suffixes treated as binary (not read as text)
_BINARY_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".docx"}


def load_knowledge(agent: Any) -> Dict[str, Any]:
    """
    Load all knowledge for an agent at initialization time.

    Loads from:
      1. shared/knowledge/              — platform-wide, all agents
      2. agents/<name>/training/knowledge/ — agent-specific

    Returns a dict:
        {
            "shared": { "<relative_path>": "<content>", ... },
            "agent":  { "<relative_path>": "<content>", ... },
        }

    Empty dicts are returned for missing directories — never raises.
    """
    knowledge: Dict[str, Any] = {}

    agent_name = _resolve_agent_name(agent)

    # 1. Shared knowledge
    if _SHARED_ROOT.exists():
        knowledge["shared"] = _load_folder(_SHARED_ROOT)
        logger.info(
            "load_knowledge: loaded %d shared knowledge file(s).",
            len(knowledge["shared"])
        )
    else:
        knowledge["shared"] = {}
        logger.debug("load_knowledge: shared knowledge path not found: %s", _SHARED_ROOT)

    # 2. Agent-specific knowledge
    agent_path = _AGENTS_ROOT / agent_name / "training" / "knowledge"
    if agent_path.exists():
        knowledge["agent"] = _load_folder(agent_path)
        logger.info(
            "load_knowledge: loaded %d agent knowledge file(s) for %s.",
            len(knowledge["agent"]), agent_name
        )
    else:
        knowledge["agent"] = {}
        logger.debug(
            "load_knowledge: agent knowledge path not found: %s", agent_path
        )

    return knowledge


# ------------------------------------------------------------------
# Internal: folder loader
# ------------------------------------------------------------------

def _load_folder(path: Path) -> Dict[str, str]:
    """
    Load all readable files in a knowledge directory recursively.

    tree-files.txt is loaded as a regular file (index artifact) — it no
    longer masks or replaces real files. knowledge_query() needs actual
    content to score relevance; a directory listing is not enough.

    .meta sidecar files are excluded — provenance only, not knowledge.
    Binary file formats are noted but not read as text.
    .docx files are extracted via pandoc if available.
    """
    docs: Dict[str, str] = {}

    for file in path.rglob("*"):
        if not file.is_file():
            continue

        suffix = file.suffix.lower()
        rel    = str(file.relative_to(path))

        # Exclude provenance sidecars
        if suffix in _EXCLUDED_SUFFIXES:
            continue

        # Binary formats — note but don't attempt text read
        if suffix in _BINARY_SUFFIXES:
            if suffix == ".docx":
                content = _read_docx(file)
                if content:
                    docs[rel] = content
                else:
                    docs[rel] = f"<docx: pandoc unavailable — {rel}>"
            else:
                docs[rel] = f"<binary: {suffix}>"
            continue

        # Text files
        try:
            docs[rel] = file.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            logger.warning("load_knowledge: could not read %s — %s", file, exc)
            docs[rel] = f"<read error: {exc}>"

    return docs


def _read_docx(path: Path) -> str:
    """
    Extract plain text from a .docx file using pandoc subprocess.
    Returns empty string if pandoc is unavailable.
    """
    import subprocess
    try:
        result = subprocess.run(
            ["pandoc", str(path), "-t", "plain", "--wrap=none"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            return result.stdout
        logger.debug("load_knowledge: pandoc failed for %s — %s", path, result.stderr)
        return ""
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        logger.debug("load_knowledge: pandoc unavailable for %s — %s", path, exc)
        return ""


# ------------------------------------------------------------------
# Internal: agent name resolver
# ------------------------------------------------------------------

def _resolve_agent_name(agent: Any) -> str:
    """
    Resolve agent name safely.
    Uses card.get() not card[] — Gap Registry fix.
    Falls back through agent.name → actor_name → class name.
    """
    card = getattr(agent, "card", {}) or {}
    return (
        card.get("name")
        or getattr(agent, "name", None)
        or getattr(agent, "actor_name", None)
        or agent.__class__.__name__
    )
