/**
 * This DarkWeb-Checker AgentCard conveys:
 * - Overall details (version, name, description, uses)
 * - Skills: A set of capabilities the agent can perform
 * - Default modalities/content types supported by the agent.
 * - AuthenticatedExtendedCard contains tasks and messages for Registered Agents
 */

/**
* DarkWeb-Checker AgentCard¶
*/
{
  "name": "DarkWeb-Checker",
  "description": "Search breach forums, marketplaces, and dark web sources for stolen PI — and collect evidence to support claims that an organization acquired or used stolen data.",
  "url": "https://privacyportfolio.com/agent-registry/darkweb-checker/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
  },
  "iconUrl": "https://privacyportfolio.com/agent-registry/darkweb-checker/darkweb-checker-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/darkweb-checker/v1-DarkWeb-Checker-AgentCard.md",
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
  "security": [
    { "yo-ai": ["apiKey", "yo-api", "header"] }
  ],
  "defaultInputModes": ["application/json", "text/plain"],
  "defaultOutputModes": ["application/json", "text/plain"],
  "skills": [
    {
      "id": "scan-darkweb",
      "name": "Scan Dark Web",
      "description": "Searches breach forums, marketplaces, and dark web sources for stolen personal information.",
      "tags": ["darkweb", "breach", "scan", "logEvent"],
      "examples": [
        "Search for email in breach dump",
        "Check if phone number appears in dark web dataset",
        "Scan for identity package listings"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "trace-data-origins",
      "name": "Trace Data Origins",
      "description": "Analyzes stolen data to infer which organization may have leaked or sold the information.",
      "tags": ["breach", "origin", "analysis", "logEvent"],
      "examples": [
        "Identify likely source of stolen data",
        "Match dataset structure to known vendor",
        "Infer breach origin"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "collect-darkweb-evidence",
      "name": "Collect Dark Web Evidence",
      "description": "Captures structured evidence of stolen PI to support complaints, deletion requests, or regulatory escalation.",
      "tags": ["evidence", "darkweb", "compliance", "logEvent"],
      "examples": [
        "Record breach listing",
        "Store dataset hash",
        "Capture seller metadata"
      ],
      "inputModes": ["application/json"],
      "outputModes": ["application/json"]
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}