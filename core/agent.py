# yo_ai_main/core/agent.py - Base Agent
# the enforcement logic lives in the Solicitor General’s tool base class and the platform runtime.

from importlib import import_module
from typing import Any, Dict, List
from pydantic import BaseModel

from yo_ai_main.core.tooling import Tool, ToolProvider


class Agent(BaseModel):
    """
    Unified base class for all Yo-ai agents.
    Loads tools, schemas, skills, and fingerprints from the AgentCard
    and optional extended card.
    """

    card: Any
    extended: Any | None = None

    # ------------------------------
    # Initialization
    # ------------------------------
    def __init__(self, card, extended_card=None):
        super().__init__(card=card, extended=extended_card)

        # Declarative contract loading
        self.skills = self._load_skills()
        self.tools = self._load_tools()
        self.schemas = self._load_schemas()
        self.fingerprints = self._load_fingerprints()

    # ------------------------------
    # Skills
    # ------------------------------
    def _load_skills(self) -> List[str]:
        skills = self.card.get("skills", [])
        if self.extended:
            skills += self.extended.get("skills", [])
        return skills

    # ------------------------------
    # Tools
    # ------------------------------
    def _load_tools(self) -> Dict[str, Tool]:
        tools = {}

        # Merge base + extended definitions
        tool_defs = self.card.get("tools", [])
        if self.extended:
            tool_defs += self.extended.get("tools", [])

        for tool_def in tool_defs:
            module_path = tool_def["path"].replace("/", ".")
            module = import_module(module_path)
            tool_class = getattr(module, tool_def["name"])

            provider = ToolProvider(**tool_def["provider"])

            tool = tool_class(
                name=tool_def["name"],
                description=tool_def.get("description", ""),
                capabilities=tool_def["capabilities"],
                provider=provider,
                config=tool_def.get("config", {})
            )

            tools[tool_def["name"]] = tool

        return tools

    # ------------------------------
    # Schemas
    # ------------------------------
    def _load_schemas(self) -> List[Dict[str, Any]]:
        schemas = self.card.get("schemas", [])
        if self.extended:
            schemas += self.extended.get("schemas", [])
        return schemas

    # ------------------------------
    # Fingerprints
    # ------------------------------
    def _load_fingerprints(self) -> Dict[str, Any]:
        fingerprints = self.card.get("fingerprints", {})
        if self.extended:
            fingerprints.update(self.extended.get("fingerprints", {}))
        return fingerprints
    

