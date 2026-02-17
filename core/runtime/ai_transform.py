# runtime/ai_transform.py
# This module is the “AI Transformation Layer.”
# It builds the reasoning prompt, calls your AI provider (LLM, Bedrock, OpenAI, Azure OpenAI, etc.), 
# and returns a structured Python object.

"""
AI Transformation Layer

Responsibilities:
- Build a structured prompt for capability execution
- Invoke the agent’s AI backend (LLM, Bedrock, Azure OpenAI, etc.)
- Return a Python dict representing the AI-generated result
"""

import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def call_ai(prompt: dict, agent):
    """
    Executes the AI transformation for a capability.

    Parameters:
        prompt (dict): {
            "persona": ...,
            "agentId": ...,
            "capability": ...,
            "input": ...,
            "context": ...,
            "instructions": ...
        }
        agent: the instantiated agent runtime (provides AI client + persona)

    Returns:
        dict: AI-generated result (unshaped)
    """

    # ------------------------------------------------------------
    # 1. Build the LLM prompt
    # ------------------------------------------------------------
    system_prompt = agent.build_system_prompt()

    user_prompt = {
        "persona": prompt.get("persona"),
        "capability": prompt.get("capability"),
        "input": prompt.get("input"),
        "context": prompt.get("context"),
        "instructions": prompt.get("instructions"),
    }

    logger.info(f"[AI] Executing capability: {prompt.get('capability')}")

    # ------------------------------------------------------------
    # 2. Call the agent’s AI backend
    # ------------------------------------------------------------
    # NOTE: agent.ai_client must be implemented by your agent runtime.
    ai_response = agent.ai_client.chat_completion(
        system=system_prompt,
        user=json.dumps(user_prompt, indent=2)
    )

    # ------------------------------------------------------------
    # 3. Parse the AI response
    # ------------------------------------------------------------
    try:
        parsed = json.loads(ai_response)
        logger.info("[AI] Parsed JSON response successfully")
        return parsed

    except Exception:
        logger.warning("[AI] Response was not valid JSON; returning raw text")
        return {"rawText": ai_response}
