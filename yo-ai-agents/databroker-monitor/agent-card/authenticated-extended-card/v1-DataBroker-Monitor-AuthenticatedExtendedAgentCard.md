/**
 * This DataBroker-Monitor Authenticated Extended Agent Card conveys:
 * - AuthenticatedExtendedCard contains tasks, messages, artifacts, and tools for Registered Agents
 * - Overall details (version, name, description, uses)
 * - Skills: A set of capabilities the agent can perform
 * - Default modalities/content types supported by the agent.
 */

/**
* DataBroker-Monitor Authenticated Extended Agent Card¶
*/
{
  "name": "DataBroker-Monitor",
  "description": "Monitors registered data brokers to detect possession, sale, or distribution of personal information and identify downstream purchasers.",
  "url": "https://privacyportfolio.com/agent-registry/databroker-monitor/auth/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
  },
  "iconUrl": "https://privacyportfolio.com/agent-registry/databroker-monitor/databroker-monitor-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/databroker-monitor/auth/v1-DataBroker-Monitor-AuthenticatedExtendedAgentCard.md",
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
  "security": [
    { "yo-ai": ["apiKey", "yo-api", "header"] }
  ],
  "defaultInputModes": ["application/json", "text/plain"],
  "defaultOutputModes": ["application/json", "text/plain"],
  "skills": [
    {
      "id": "scan-broker-inventory",
      "name": "Scan Broker Inventory",
      "description": "Searches registered data broker datasets for matches to minimized PI bundles provided by the Data-Steward.",
      "tags": ["broker", "scan", "inventory", "logEvent"],
      "examples": [
        "Search for email in broker dataset",
        "Check if phone number appears in broker feed",
        "Scan for profile matches"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "identify-downstream-vendors",
      "name": "Identify Downstream Vendors",
      "description": "Determines which vendors are purchasing data from brokers and using it to make automated decisions.",
      "tags": ["vendors", "broker", "downstream", "logEvent"],
      "examples": [
        "Identify vendor purchasing my data",
        "Check if broker sold data to advertiser",
        "Map broker → vendor relationships"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "collect-broker-evidence",
      "name": "Collect Broker Evidence",
      "description": "Captures structured evidence of broker possession or sale of personal information for use in complaints or deletion requests.",
      "tags": ["evidence", "broker", "compliance", "logEvent"],
      "examples": [
        "Record broker match",
        "Store dataset reference",
        "Capture sale metadata"
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