/**
 * This Decision-Master AgentCard conveys:
 * - Overall details (version, name, description, uses)
 * - Skills: A set of capabilities the agent can perform
 * - Default modalities/content types supported by the agent.
 * - Authentication requirements
 */

/**
* Decision-Master AgentCard¶
*/
{
  "name": "Decision-Master",
  "description": "The Decision-Master agent identifies and analyzes decision-making events in event logs and publishes them to the Decision-Diary topic.",
  "url": "https://privacyportfolio.com/agent-registry/decision-master/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://privacyportfolio.com"
  },
  "iconUrl": "https://privacyportfolio.com/agent-registry/decision-master/decision-master-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/decision-master/v1-Decision-Master-AgentCard.md",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "securitySchemes": {
    "yo-ai": {
      "type": "apiKey",
      "name": "yo-api",
      "in": "header"
    }
  },
  "security": [{ "yo-ai": ["apiKey", "yo-api", "header"] }],
  "defaultInputModes": ["application/json", "text/plain"],
  "defaultOutputModes": ["application/json", "text/plain"],
  "skills": [
    {
      "id": "manage-Decision-Diary",
      "name": "manage-Decision-Diary",
      "description": "Add, remove, correlate, and prune events associated with decision sets.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "log_ref": { "type": "string" },
          "decision_ref": { "type": "string" },
          "factors": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["log_ref", "decision_ref", "factors"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "decision_ref": { "type": "string" },
          "log_ref": { "type": "string" },
          "decision_factors": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    {
      "id": "identify-Decision-Events",
      "name": "identify-Decision-Events",
      "description": "Identifies likely decision-making events.",
      "tags": ["approval", "denial", "no-decision"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "log_ref": { "type": "string" },
          "factors": {
            "type": "array",
            "items": { "type": "string" }
          },
          "decision-indicators": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["log_ref", "factors", "decision-indicators"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "decision_findings": {
            "type": "array",
            "items": { "type": "string" }
          },
          "recommended_actions": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    {
      "id": "identify-Decision-Outcome",
      "name": "identify-Decision-Outcome",
      "description": "Identifies the outcome of each decision-set.",
      "tags": ["approval", "denial", "no-decision"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "log_ref": { "type": "string" },
          "decision-set_ref": { "type": "string" },
          "decision-outcomes": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["log_ref", "decision-set_ref", "decision-set_ref"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "decision-set_ref": { "type": "string" },
          "decision-set-outcome": { "type": "string" }
      }
    },
    {
      "id": "analyze-ApprovalOrDenial",
      "name": "analyze-ApprovalOrDenial",
      "description": "Analyzes explanation of decision-set outcome based on decision factors, evidence, and applicable mandates.",
      "tags": ["approval", "denial", "no-decision"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "decision-set_ref": { "type": "string" },
          "decision-set-outcome": { "type": "string" }
          "org_ref": { "type": "string" }, 
          "mandates": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["org_ref", "facts"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "liability_findings": {
            "type": "array",
            "items": { "type": "string" }
          },
          "recommended_actions": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}
