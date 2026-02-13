# yo_ai_main/a2a/registry.py - agent registry for FastA2A


from typing import Dict, Optional
from yo_ai_main.core.platform_agent import PlatformAgent


class AgentRegistry:
    """
    In-memory registry of active agent instances.
    Used by the Solicitor-General and FastA2A runtime
    to route requests to the correct agent.
    """

    _agents: Dict[str, PlatformAgent] = {}

    @classmethod
    def register(cls, agent_id: str, agent: PlatformAgent) -> None:
        cls._agents[agent_id] = agent

    @classmethod
    def get(cls, agent_id: str) -> Optional[PlatformAgent]:
        return cls._agents.get(agent_id)

    @classmethod
    def all(cls) -> Dict[str, PlatformAgent]:
        return dict(cls._agents)

    @classmethod
    def exists(cls, agent_id: str) -> bool:
        return agent_id in cls._agents