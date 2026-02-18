# Solicitor-General’s Just Ask Capability
# This is the SG’s “help” command — 
# show the longer introduction when an agent explicitly asks for guidance.

# Inside Solicitor-General class, add this:

async def handle_capability(self, capability: str, payload: dict, context: dict):
    if capability == "Just-Ask":
        return self._just_ask()
    # fallback for other SG capabilities
    return {"message": f"Unknown SG capability: {capability}"}

def _just_ask(self):
    return {
        "introduction": (
            "Welcome to the Yo ai Platform. I am the Solicitor General, the "
            "coordination and governance agent responsible for routing, "
            "correlation, negotiation, and task lifecycle management across "
            "all agents in this ecosystem."
        ),
        "what_you_can_do": [
            "Announce your intent",
            "Request a capability (e.g., Data Steward.Normalize)",
            "Ask which agents are available",
            "Begin or resume a task",
            "Explore platform conventions",
        ],
        "next_steps": (
            "State your intent or request a capability and I will assist you."
        ),
    }
