# agent.py
# This class is intentionally simple — 
# the enforcement logic lives in the Solicitor General’s tool base class and the platform runtime.

class Agent:
    """
    Unified base class for all Yo-ai agents.
    The platform determines which cards are provided.
    """
    def __init__(self, card, extended_card=None):
        self.card = card
        self.extended = extended_card

        # Declarative contract loading
        self.skills = self._load_skills()
        self.tools = self._load_tools()
        self.schemas = self._load_schemas()
        self.fingerprints = self._load_fingerprints()

    # ------------------------------
    # Internal loaders (stubs)
    # ------------------------------

    def _load_skills(self):
        return self.card.get("skills", [])

    def _load_tools(self):
        tools = self.card.get("tools", [])
        if self.extended:
            tools += self.extended.get("tools", [])
        return tools

    def _load_schemas(self):
        schemas = self.card.get("schemas", [])
        if self.extended:
            schemas += self.extended.get("schemas", [])
        return schemas

    def _load_fingerprints(self):
        return self.card.get("fingerprints", {})
