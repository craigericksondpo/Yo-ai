# yo-ai_agent.py

from agent import Agent

class YoAiAgent(Agent):
    """
    Yo-ai agents may or may not receive an extended card,
    depending on authentication and policy.
    """
    def __init__(self, card, extended_card=None):
        super().__init__(card, extended_card)
