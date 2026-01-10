/**
 * This Vendor-Manager AgentCard conveys:
 * - Overall details (version, name, description, uses)
 * - Skills: A set of capabilities the agent can perform
 * - Default modalities/content types supported by the agent.
 * - Authentication requirements
 */

/**
* Vendor-Manager AgentCard¶
*/
{
  "name": "Vendor-Manager",
  "description": "Agent responsible for monitoring vendors to maintain Responsible AI certification status.",
  "url": "https://privacyportfolio.com/agent-registry/vendor-manager/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
    },
  "iconUrl": "https://privacyportfolio.com/agent-registry/vendor-manager/vendor-manager-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/vendor-manager/v1-Vendor-Manager-AgentCard.md",
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
      "id": "manage-OrgProfile",
      "name": "manage-OrgProfile",
      "description": "Manage an organization profile as a resource (not as an agent).",
      "tags": ["verifyOrg", "shareData", "createTask", "buildWorkflow", "logEvent"],
      "examples": [
        "Identify the incorporated entity",
        "Get terms and conditions",
        "Send request"
      ],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": ["application/json", "text/plain"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "org_ref": {
            "type": "string",
            "description": "Opaque identifier for the organization (name, ID, DUNS, etc.)."
          },
          "operation": {
            "type": "string",
            "enum": [
              "verify",
              "fetch_terms",
              "share_data",
              "create_task",
              "build_workflow",
              "log_event"
            ]
          },
          "payload": {
            "type": "object",
            "description": "Operation-specific data."
          }
        },
        "required": ["org_ref", "operation"]
      }
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}