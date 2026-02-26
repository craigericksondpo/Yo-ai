# core/runtime/knowledge_write.py

from pathlib import Path
from datetime import datetime
from typing import Any


SHARED_ROOT = Path("shared/knowledge")


def add_shared_knowledge(registered_agent: Any, filename: str, content: str, *, overwrite: bool = False) -> Path:
    """
    Add or update a file in the shared knowledge repository.

    Requires a RegisteredAgent object (Door-Keeper validated).
    """

    if not hasattr(registered_agent, "agent_name"):
        raise PermissionError("Only a RegisteredAgent may update shared knowledge.")

    SHARED_ROOT.mkdir(parents=True, exist_ok=True)

    target = SHARED_ROOT / filename

    if target.exists() and not overwrite:
        raise FileExistsError(f"Shared knowledge file already exists: {filename}")

    # Write content
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    # Append provenance metadata
    _write_provenance(target, registered_agent.agent_name)

    return target


def add_agent_knowledge(agent: Any, filename: str, content: str, *, overwrite: bool = False) -> Path:
    """
    Add or update a file in the agent-specific knowledge repository.

    Only the agent instance itself may update its own knowledge.
    """

    agent_name = _resolve_agent_name(agent)
    root = Path(f"agents/{agent_name}/training/knowledge")
    root.mkdir(parents=True, exist_ok=True)

    target = root / filename

    if target.exists() and not overwrite:
        raise FileExistsError(f"Agent knowledge file already exists: {filename}")

    # Write content
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    # Append provenance metadata
    _write_provenance(target, agent_name)

    return target


def _resolve_agent_name(agent: Any) -> str:
    card = getattr(agent, "card", {}) or {}
    return card.get("name") or agent.__class__.__name__


def _write_provenance(target: Path, actor_name: str):
    """
    Write a sidecar provenance file:
        <filename>.meta
    containing:
        - who wrote it
        - when
        - path
    """

    meta = target.with_suffix(target.suffix + ".meta")

    timestamp = datetime.utcnow().isoformat() + "Z"

    meta.write_text(
        f"actor: {actor_name}\n"
        f"timestamp: {timestamp}\n"
        f"path: {target}\n",
        encoding="utf-8"
    )
