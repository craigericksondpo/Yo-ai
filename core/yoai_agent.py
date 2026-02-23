# core/yoai_agent.py

from core.agent import Agent
from core.runtime.load_fingerprints import load_fingerprints
from core.runtime.load_knowledge import load_knowledge
from core.tooling import Tool, ToolProvider
from importlib import import_module


class YoAiAgent(Agent):
    """
    YoAiAgent:
    Identity-bearing, profile-aware, multi-instance agent.

    Responsibilities:
      - Load skills, tools, schemas from card + extended card
      - Load runtime artifacts (fingerprints, knowledge)
      - Accept optional profile injection
      - Provide context-building helpers for capability execution

    No agent_id field — identity is derived from the AgentCard.
    """

    def __init__(self, *, card, extended_card=None, profile=None, context=None):
        super().__init__(card=card, extended_card=extended_card, context=context)

        # Profile injection (optional)
        self.profile = profile

        # Declarative contract loading
        self.skills = self._load_skills()
        self.tools = self._load_tools()
        self.schemas = self._load_schemas()

        # Runtime artifacts
        self.fingerprints = load_fingerprints(self.card, self.extended)
        self.knowledge = load_knowledge(self)

    # ------------------------------------------------------------------
    # Loader: Skills
    # ------------------------------------------------------------------
    def _load_skills(self):
        skills = list(self.card.get("skills", []))
        if self.extended:
            skills += self.extended.get("skills", [])
        return skills

    # ------------------------------------------------------------------
    # Loader: Tools
    # ------------------------------------------------------------------
    def _load_tools(self):
        tools = {}
        tool_defs = list(self.card.get("tools", []))
        if self.extended:
            tool_defs += self.extended.get("tools", [])

        for tool_def in tool_defs:
            module_path = tool_def["path"].replace("/", ".")
            module = import_module(module_path)
            tool_class = getattr(module, tool_def["name"])
            provider = ToolProvider(**tool_def["provider"])

            tools[tool_def["name"]] = tool_class(
                name=tool_def["name"],
                description=tool_def.get("description", ""),
                capabilities=tool_def["capabilities"],
                provider=provider,
                config=tool_def.get("config", {})
            )
        return tools

    # ------------------------------------------------------------------
    # Loader: Schemas
    # ------------------------------------------------------------------
    def _load_schemas(self):
        schemas = list(self.card.get("schemas", []))
        if self.extended:
            schemas += self.extended.get("schemas", [])
        return schemas