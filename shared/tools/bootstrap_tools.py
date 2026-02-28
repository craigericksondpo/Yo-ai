# shared/tools/bootstrap_tools.py

import json
from importlib import import_module
from shared.tools.tool_registry import ToolRegistry

def build_tool_registry(extended_card: dict | None) -> ToolRegistry:
    registry = ToolRegistry()

    if not extended_card:
        return registry

    for tool_def in extended_card.get("x-tools", []):
        tool_name = tool_def["name"]

        module_path = tool_def["path"].replace("/", ".")
        class_name = tool_def["class"]

        module = import_module(module_path)
        adapter_class = getattr(module, class_name)

        provider_cfg = tool_def.get("provider", {})
        config_cfg = tool_def.get("config", {})

        adapter_instance = adapter_class(
            provider=provider_cfg,
            config=config_cfg,
        )

        registry.register(tool_name, adapter_instance)

    return registry

# Optional standalone usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python bootstrap_tools.py <extended_agent_card.json>")
        sys.exit(1)

    path = sys.argv[1]

    with open(path, "r") as f:
        extended_card = json.load(f)

    registry = build_tool_registry(extended_card)

    print("Tools loaded:")
    for name in registry.tools.keys():
        print(f" - {name}")
