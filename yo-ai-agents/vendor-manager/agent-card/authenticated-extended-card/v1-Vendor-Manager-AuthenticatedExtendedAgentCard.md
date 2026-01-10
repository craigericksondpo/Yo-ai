/**
 * This Vendor-Manager Authenticated Extended Card conveys:
 * - AuthenticatedExtendedCard contains tasks, messages, artifacts, and tools for Registered Agents.
 * - Tasks: A task encapsulates the entire interaction related to a specific goal or request.
 * - Messages: Messages are used for instructions, prompts, replies, and status updates.
 * - Artifacts: Collection of artifacts created by the agent.
 */

/**
* Vendor-Manager Authenticated Extended Agent Card¶
*/
{
  "name": "Vendor-Manager",
  "description": "Agent responsible for monitoring vendors to maintain Responsible AI certification status.",
  "url":   "https://privacyportfolio.com/agent-registry/vendor-manager/auth/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
    },
  "iconUrl": "https://privacyportfolio.com/agent-registry/vendor-manager/vendor-manager-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/vendor-manager/auth/v1-Vendor-Manager-AuthenticatedExtendedAgentCard.md",
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
  "x-tasks": [
    {
      "taskType": "artifact.validate",
      "description": "Validate an artifact and produce a compliance-grade validation report.",
      "inputSchema": { "$ref": "#/schemas/ArtifactValidationInput" },
      "outputSchema": { "$ref": "#/schemas/ArtifactValidationOutput" }
    },
    {
      "taskType": "evidence.publish",
      "description": "Publish a signed evidence manifest for downstream agents.",
      "inputSchema": { "$ref": "#/schemas/EvidenceManifestInput" },
      "outputSchema": { "$ref": "#/schemas/EvidenceManifestOutput" }
    }
  ],
  "x-tools": [
    {
      "name": "http.get",
      "description": "Performs authenticated GET requests to fetch external resources.",
      "inputSchema": { "$ref": "#/schemas/HttpGetInput" },
      "outputSchema": { "$ref": "#/schemas/HttpGetOutput" },
      "auth": "apiKey"
    },
    {
      "name": "crypto.sign",
      "description": "Signs payloads using the agent's internal key material.",
      "inputSchema": { "$ref": "#/schemas/CryptoSignInput" },
      "outputSchema": { "$ref": "#/schemas/CryptoSignOutput" },
      "auth": "none"
    }
  ],
  "x-messages": [
    {
      "messageType": "artifact.validated",
      "direction": "emit",
      "description": "Emitted when an artifact has been validated.",
      "schema": { "$ref": "#/schemas/ArtifactValidatedEvent" }
    },
    {
      "messageType": "evidence.published",
      "direction": "emit",
      "description": "Emitted when an evidence manifest is published.",
      "schema": { "$ref": "#/schemas/EvidencePublishedEvent" }
    }
  ],
  "x-artifacts": [
    {
      "artifactType": "evidence.manifest",
      "description": "A cryptographically signed manifest describing evidence, lineage, and provenance.",
      "schema": { "$ref": "#/schemas/EvidenceManifest" },
      "mediaType": "application/json"
    },
    {
      "artifactType": "validation.report",
      "description": "A compliance-grade validation report for artifacts.",
      "schema": { "$ref": "#/schemas/ValidationReport" },
      "mediaType": "application/json"
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}  
