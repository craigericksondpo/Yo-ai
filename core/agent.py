# core/agent.py
from pydantic import BaseModel

class Agent(BaseModel):
    """
    Visiting Agent Proxy.
    Base class for all 'visiting agents' that come to the platform.
    This wrapper class is intentionally minimal — 
    it loads only the metadata that is safe for external agents to declare (skills)..
    """

    card: dict
    extended: dict | None = None
    context: dict | None = None

    def __init__(self, *, card, extended_card=None, context=None, **kwargs):
        super().__init__(card=card, extended=extended_card, context=context, **kwargs)

        # Visiting agents may declare skills; load them if present.
        self.skills = self._load_skills()

    # ---------------------------------------------------------
    # Skills (safe for visiting agents)
    # ---------------------------------------------------------
    def _load_skills(self):
        skills = list(self.card.get("skills", []))
        if self.extended:
            skills += self.extended.get("skills", [])
        return skills