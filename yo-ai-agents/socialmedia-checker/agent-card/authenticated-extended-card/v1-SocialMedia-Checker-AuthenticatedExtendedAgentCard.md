/**
 * This SocialMedia-Checker AuthenticatedExtendedCard conveys:
 * - AuthenticatedExtendedCard contains tasks, messages, artifacts, and tools for Registered Agents.
 * - Tasks: A task encapsulates the entire interaction related to a specific goal or request.
 * - Messages: Messages are used for instructions, prompts, replies, and status updates.
 * - Artifacts: Collection of artifacts created by the agent.
 */

/**
* SocialMedia-Checker Authenticated Extended Agent Card¶
*/
{
  "name": "SocialMedia-Checker",
  "description": "Evaluates social media activity to verify promotional requirements and detect potential misappropriation of personal data.",
  "url": "https://privacyportfolio.com/agent-registry/socialmedia-checker/auth/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
  },
  "iconUrl": "https://privacyportfolio.com/agent-registry/socialmedia-checker/socialmedia-checker-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/socialmedia-checker/auth/v1-SocialMedia-Checker-SocialMedia-Checker-AuthenticatedExtendedAgentCard.md",
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
      "id": "verify-promo-engagement",
      "name": "Verify Promotional Engagement",
      "description": "Checks whether required social media actions (follow, like, repost, hashtag usage) were completed for promotional eligibility.",
      "tags": ["promotion", "verification", "rewards", "logEvent"],
      "examples": [
        "Verify user followed brand",
        "Check hashtag usage",
        "Confirm engagement for reward eligibility"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "detect-misappropriation",
      "name": "Detect Misappropriated Data",
      "description": "Searches social media for unauthorized use of personal information, impersonation, or leaked data indicators.",
      "tags": ["misappropriation", "fraud", "identity", "logEvent"],
      "examples": [
        "Search for impersonation accounts",
        "Detect leaked email or phone number",
        "Identify suspicious mentions of PI"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "collect-evidence",
      "name": "Collect Evidence",
      "description": "Captures structured evidence of misappropriation or promotional compliance for downstream agents.",
      "tags": ["evidence", "compliance", "logEvent"],
      "examples": [
        "Capture screenshot metadata",
        "Record engagement proof",
        "Store impersonation indicators"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
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