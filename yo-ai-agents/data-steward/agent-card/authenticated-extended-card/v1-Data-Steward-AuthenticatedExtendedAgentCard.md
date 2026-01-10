/**
 * This Data-Steward AuthenticatedExtendedCard conveys:
 * - AuthenticatedExtendedCard contains tasks, messages, artifacts, and tools for Registered Agents.
 * - Tasks: A task encapsulates the entire interaction related to a specific goal or request.
 * - Messages: Messages are used for instructions, prompts, replies, and status updates.
 * - Artifacts: Collection of artifacts created by the agent.
 */

/**
* Data-Steward Authenticated Extended Agent Card¶
*/

{
  "name": "Data-Steward",
  "description": "Governs access to the personal data vault, evaluates intended use of personal data, and makes decisions and takes action on behalf of an individual person.",
  "url": "https://privacyportfolio.com/agent-registry/data-steward/auth/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
  },
  "iconUrl": "https://privacyportfolio.com/agent-registry/data-steward/data-steward-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/data-steward/auth/v1-Data-Steward-AuthenticatedExtendedAgentCard.md",
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
      "id": "answer-phone",
      "name": "Answer Phone",
      "description": "Handle inbound phone calls, verify caller identity, and determine purpose of call.",
      "tags": ["verifyCaller", "shareData", "createTask", "buildWorkflow", "logEvent"],
      "examples": [
        "Identify the caller",
        "Introduce yourself",
        "Determine purpose of call"
      ],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": ["application/json", "text/plain"]
    },
    {
      "id": "call-phone",
      "name": "Call Phone",
      "description": "Make outbound phone calls for verification, negotiation, or rights requests.",
      "tags": ["pushNotification", "request", "verify", "question", "survey", "logEvent"],
      "examples": [
        "YourRequestStatus",
        "Please do this",
        "Buy this",
        "Do you have?",
        "Answer these questions"
      ],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": ["application/json", "text/plain"]
    },
    {
      "id": "govern-data-requests",
      "name": "Govern Data Requests",
      "description": "Evaluate intended use of personal data before granting access to the personal data vault.",
      "tags": ["verify", "authorize", "policyCheck", "riskAssessment", "logEvent"],
      "examples": [
        "Request to fill out a signup form",
        "Request to provide shipping address",
        "Request to verify identity"
      ],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": ["application/json", "text/plain"]
    },
    {
      "id": "send-email",
      "name": "Send Email",
      "description": "Send outbound email as the authorized agent of the data subject.",
      "tags": ["pushNotification", "request", "verify", "solicitation", "logEvent"],
      "examples": [
        "YourRequestStatus",
        "Please do this",
        "Buy this",
        "Do you have?",
        "Answer these questions"
      ],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": ["application/json", "text/plain"]
    },
    {
      "id": "read-email",
      "name": "Read Email",
      "description": "Read inbound email, detect spam/phishing, and extract workflow triggers.",
      "tags": ["spam", "phishing", "solicitation", "verify", "survey", "logEvent"],
      "examples": [
        "Your Request Status",
        "Please do this",
        "Buy this",
        "Do you have?",
        "I am..."
      ],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": ["application/json", "text/plain"]
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