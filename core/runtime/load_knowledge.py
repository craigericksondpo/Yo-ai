# core/runtime/load_knowledge.py

import os
from pathlib import Path

def load_knowledge(agent):
    """
    Load knowledge from:
      - /shared/knowledge/
      - agents/<agent-name>/training/knowledge/
    Supports:
      - real files (html, pdf, md, txt, etc.)
      - tree-files.txt metadata-only representations
    """

    knowledge = {}

    # 1. Load shared knowledge
    shared_path = Path("shared/knowledge")
    if shared_path.exists():
        knowledge["shared"] = _load_folder(shared_path)

    # 2. Load agent-specific knowledge
    agent_path = Path(f"agents/{agent.card['name']}/training/knowledge")
    if agent_path.exists():
        knowledge["agent"] = _load_folder(agent_path)

    return knowledge


def _load_folder(path: Path):
    """
    Load either:
      - actual files
      - or tree-files.txt metadata
    """
    tree_file = path / "tree-files.txt"

    if tree_file.exists():
        return _parse_tree_file(tree_file)

    return _load_real_files(path)


def _parse_tree_file(tree_file: Path):
    """
    Parse directory metadata only.
    """
    with open(tree_file, "r") as f:
        return {"tree": f.read()}


def _load_real_files(path: Path):
    """
    Load actual file contents.
    """
    docs = {}
    for file in path.rglob("*"):
        if file.is_file():
            try:
                docs[str(file.relative_to(path))] = file.read_text(errors="ignore")
            except Exception:
                docs[str(file.relative_to(path))] = "<binary file>"
    return docs
