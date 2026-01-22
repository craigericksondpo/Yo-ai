# vendor-manager.py

import json
from datetime import datetime, timezone
from importlib import import_module
from importlib import resources
from types import MethodType
from typing import Dict, Any
from tools.tool_provider import ToolProvider

from yoai_agent import YoAiAgent

class VendorManagerAgent(YoAiAgent):
    """
    Vendor-Manager is a Yo-ai internal agent.
    It is NOT a platform agent and does not have platform privileges.
    It may receive an extended card only after authentication.
    """

    def __init__(self, card, extended_card=None):
        super().__init__(card, extended_card)  
        self.card = card

        # Load skills
        self.skills = self._load_skills()

        # Load tools
        self.tools = self._load_tools()

        # Bind event emitter if present
        self.events = self.tools.get("EventEmitter")

        # Load event schemas
        self.event_schemas = self._load_event_schemas()

        # Load internal tasks
        self.internal_tasks = self._load_internal_tasks()

        # Emit AgentStarted
        if self.events:
            self._emit(
                "AgentStarted",
                {
                    "agentId": self.card.agentId,
                    "agentType": self.card.agentType,
                    "toolsLoaded": list(self.tools.keys()),
                    "schemasLoaded": list(self.event_schemas.keys()),
                    "internalTasksLoaded": list(self.internal_tasks.keys())
                }
            )

    # ----------------------------------------------------------------------
    # Tool loading
    # ----------------------------------------------------------------------
    def _load_tools(self):
        tools = {}

        for tool_def in self.card.x_tools:
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


    # ----------------------------------------------------------------------
    # Skills loading
    # ----------------------------------------------------------------------
    def _load_skills(self):
        skills = {}
        for skill in self.card["skills"]:
            name = skill["name"]
            impl = self.extended["x-impl"][name]["handler"]
            module_name, func_name = impl.rsplit(".", 1)
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            skills[name] = MethodType(func, self)
        return skills


    # ----------------------------------------------------------------------
    # Artifact (event schema) loading
    # ----------------------------------------------------------------------
    def _load_event_schemas(self):
        schemas = {}

        for artifact in self.card.x_artifacts:
            schema_path = artifact["path"].replace("/", ".")
            module_name, file_name = schema_path.rsplit(".", 1)

            with resources.open_text(module_name, file_name) as f:
                schemas[artifact["name"]] = json.load(f)

        return schemas

    # ----------------------------------------------------------------------
    # Internal task loading
    # ----------------------------------------------------------------------
    def _load_internal_tasks(self):
        tasks = {}

        for task_def in self.card.x_tasks:
            module_path = task_def["path"].replace("/", ".")
            module = import_module(module_path)
            task_fn = getattr(module, task_def["name"])
            tasks[task_def["name"]] = task_fn

        return tasks

    # ----------------------------------------------------------------------
    # Event emission helper
    # ----------------------------------------------------------------------
    def _emit(self, event_type: str, detail: dict):
        if not self.events:
            return

        schema = self.event_schemas.get(event_type)

        # Optional: validate detail against schema
        if schema:
            self._validate_event(detail, schema)

        event = {
            "eventType": event_type,
            "sourceAgent": self.card.agentId,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "detail": detail
        }

        self.events.run(event=event)

    def _validate_event(self, detail, schema):
        # Placeholder for JSON schema validation
        # You can integrate jsonschema.validate() here
        pass

