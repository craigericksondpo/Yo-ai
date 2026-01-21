/**
 * This Workflow-Builder AuthenticatedExtendedCard conveys:
 * - AuthenticatedExtendedCard contains tasks, messages, tools, and artifacts for Registered Agents
 * - Tasks: A task encapsulates the entire interaction related to a specific goal or request.
 * - Messages: Messages are used for instructions, prompts, replies, and status updates.
 * - Artifacts: Collection of artifacts created by the agent.
 */

/**
* Workflow-Builder Authenticated Extended AgentCard¶
*/
{
  "name": "Workflow-Builder",
  "description": "Agent that builds workflow itineraries connecting agents with endpoints.",
  "url": "https://privacyportfolio.com/agent-registry/workflow-builder/auth/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
    },
  "iconUrl": "https://privacyportfolio.com/agent-registry/workflow-builder/workflow-builder-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/workflow-builder/auth/Workflow-Builder-AuthenticatedExtendedAgentCard.md",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true,
    "exposesTasks": true,
    "exposesMessages": true,
    "exposesArtifacts": true,
    "exposesTools": true
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
  "defaultOutputModes": ["application/json", "image/png"],
    "skills": [
        {"name": "Workflow.Build"}
    ],
    "x-capabilities": [
        {
          "Workflow.Build": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "Workflow.Build"}},
                  {"artifact": {"type": "task", "name": "Workflow.Build"}},
                  {"artifact": {"type": "tool", "name": "Workflow.Build"}},
                  {"artifact": {"type": "handler", "name": "Workflow.Build"}},
                  {"artifact": {"type": "messageType", "name": "Workflow.Build.Input"}},
                  {"artifact": {"type": "messageType", "name": "Workflow.Build.Output"}}
              ]
          }
        }
    ],
    "x-artifacts": [
        {
        "name": "Workflow.Build",
        "version": "1.0.0",
        "artifactType": "skill",
        "description": "Builds orchestrated workflows connecting agents with endpoints.",
        "tags": ["-wf", "internal", "external"]
        },
        {
        "name": "Workflow.Build",
        "version": "1.0.0",
        "artifactType": "task",
        "description": "Builds orchestrated workflows connecting agents with endpoints.",
        "tags": ["-wf", "internal", "external"]
        },
        {
        "name": "Workflow.Build",
        "version": "1.0.0",
        "artifactType": "tool",
        "description": "Builds orchestrated workflows connecting agents with endpoints.",
        "capabilities": ["build"],
        "path": "/",
        "provider": {
            "name": "PrivacyPortfolio",
            "brand": "Yo-ai",
            "product": "",
            "version": "1.0.0",
            "license": "Yo-ai Internal",
            "url": "https://yo-ai.ai/docs/Workflow.Build.html",
            "config": {
            "backend": ""
            }
        },
        "inputSchema": { "$ref": "#/schemas/Workflow.Build.Input" },
        "outputSchema": { "$ref": "#/schemas/Workflow.Build.Output" },
        "auth": "apiKey"
        },
        {
        "name": "Workflow.Build",
        "version": "1.0.0",
        "artifactType": "handler",
        "description": "Interface for integrating with tool executable.",
        "path": "/"
        },
        {
        "name": "Workflow.Build.Input",
        "version": "1.0.0",
        "artifactType": "messageType",
        "schema": { "$ref": "#/schemas/Workflow.Build#/definitions/Input" },
        "description": "Input schema for ."
        },
        {
        "name": "Workflow.Build.Output",
        "version": "1.0.0",
        "artifactType": "messageType",
        "schema": { "$ref": "#/schemas/Workflow.Build#/definitions/Output" },
        "description": "Output schema for ."
        }
    ],
    "supportsAuthenticatedExtendedCard": true
}