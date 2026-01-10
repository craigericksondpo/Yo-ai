/**
 * This Rewards-Seeker AuthenticatedExtendedCard conveys:
 * - AuthenticatedExtendedCard contains tasks, messages, artifacts, and tools for Registered Agents.
 * - Tasks: A task encapsulates the entire interaction related to a specific goal or request.
 * - Messages: Messages are used for instructions, prompts, replies, and status updates.
 * - Artifacts: Collection of artifacts created by the agent.
 */


/**
* Rewards-Seeker Authenticated Extended Agent Card¶
*/
{
  "name": "Rewards-Seeker",
  "description": "Agent responsible for managing loyalty programs, rewards, cashback, and promotional eligibility. Uses SocialMedia-Checker for promotional verification.",
  "url": "https://privacyportfolio.com/agent-registry/rewards-seeker/auth/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
  },
  "iconUrl": "https://privacyportfolio.com/agent-registry/rewards-seeker/rewards-seeker-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/rewards-seeker/auth/v1-Rewards-Seeker-AuthenticatedExtendedAgentCard.md",
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
      "id": "discover-rewards",
      "name": "Discover Rewards",
      "description": "Identify loyalty opportunities, cashback offers, and promotional benefits.",
      "tags": ["rewards", "loyalty", "opportunity", "logEvent"],
      "examples": [
        "Find cashback offers",
        "Identify loyalty bonuses",
        "Scan for reward-eligible purchases"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "verify-promo-eligibility",
      "name": "Verify Promo Eligibility",
      "description": "Use SocialMedia-Checker to confirm promotional requirements.",
      "tags": ["promotion", "verification", "socialMedia", "logEvent"],
      "examples": [
        "Check if user followed brand",
        "Verify hashtag usage",
        "Confirm social engagement"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "redeem-reward",
      "name": "Redeem Reward",
      "description": "Redeem loyalty points, cashback, or promotional credits.",
      "tags": ["redeem", "loyalty", "reward", "logEvent"],
      "examples": [
        "Redeem points",
        "Apply cashback",
        "Claim promotional credit"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "request-profile",
      "name": "Request Rewards Profile",
      "description": "Request minimized loyalty profile from Data-Steward.",
      "tags": ["requestData", "loyalty", "logEvent"],
      "examples": [
        "Request loyalty IDs",
        "Request reward preferences"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "discover-rewards",
      "name": "Discover Rewards",
      "description": "Returns a list of rewards programs offered by each organization.",
      "tags": ["rewards", "incentives", "points", "loyalty", "terms"],
      "examples": [
        "Find possible rewards for consumers from 'Organization Name' at 'https://orgdomain/'.",
        "{\"org\": {\"name\": "Organization Name", \"url\": \"https://orgdomain/\"}, 
         \"reward-preferences\": [\"financial\"]}"
      ],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": ["application/json", "application/vnd.geo+json", "text/html"]
    },
    {
      "id": "redemption-plan",
      "name": "Redemption Plan",
      "description": "Generates custom plan for earning and redeeming rewards based on user-defined preferences. Can include multiple rewards.",
      "tags": ["qualifications", "terms", "restrictions", "automated decisions"],
      "examples": [
        "Generate a plan to earn rewards including what to track and how to improve my odds of redeeming rewards.",
        "Rank which rewards programs I am most likely to qualify for and redeem, the organizations offering them, 
        and the estimated reward value."
      ],
      "inputModes": ["application/json"],
      "outputModes": ["image/png", "image/jpeg", "application/json", "text/html"]
    },
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