/**
 * This IP-Inspector AgentCard conveys:
 * - Overall details (version, name, description, uses)
 * - Skills: A set of capabilities the agent can perform
 * - Default modalities/content types supported by the agent.
 * - Authentication requirements
 */

/**
* IP-Inspector AgentCard¶
*/
{
  "name": "IP-Inspector",
  "description": "Discovers intellectual property and potential use cases, and searches for implementation instances.",
  "url": "https://privacyportfolio.com/agent-registry/ip-inspector/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
    },
  "iconUrl": "https://privacyportfolio.com/agent-registry/ip-inspector/ip-inspector-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/ip-inspector/v1-IP-Inspector-AgentCard.md",
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
      "name": "discover-ip-assets",
      "description": "Identifies patents, trademarks, copyrights, trade dress, and proprietary technologies associated with an entity.",
      "tags": ["patents", "trademarks", "copyrights", "ipDiscovery", "portfolioAnalysis"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "List all patents held by Company X",
        "What trademarks does this brand own"
      ]
    },
    {
      "name": "map-ip-to-products",
      "description": "Determines which products, services, or features implement or rely on specific IP assets.",
      "tags": ["productMapping", "implementationDiscovery", "ipUsage", "portfolioLinkage"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "Which products use Patent US-XXXXXXX",
        "What patents does this proprietary service rely on"
      ]
    },
    {
      "name": "search-implementation-instances",
      "description": "Searches for real-world implementations of an IP asset across products, SDKs, APIs, documentation, marketing materials, and technical artifacts.",
      "tags": ["implementationSearch", "competitiveIntelligence", "techDiscovery"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "Where is this patented method implemented",
        "Find instances of this algorithm in the vendor’s ecosystem"
      ]
    },
    {
      "name": "infer-use-cases",
      "description": "Analyzes IP assets to infer potential applications, commercial uses, and strategic value.",
      "tags": ["useCaseInference", "strategicAnalysis", "innovationMapping"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json", "text/plain"],
      "examples": [
        "What could this patent be used for",
        "Infer use cases for this portfolio"
      ]
    },
    {
      "name": "cluster-ip-portfolio",
      "description": "Groups IP assets into themes, technologies, or product domains to reveal strategic clusters.",
      "tags": ["portfolioClustering", "taxonomy", "classification", "strategicThemes"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Cluster this company’s patents into technology areas",
        "Group trademarks by product line"
      ]
    },
    {
      "name": "generate-ip-report",
      "description": "Produces a structured, regulator-friendly report summarizing discovered IP, implementations, inferred use cases, and strategic insights.",
      "tags": ["reporting", "audit", "documentation", "evidence"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json", "text/plain"],
      "examples": [
        "Create an IP summary for Company X",
        "Generate a report of patents used in proprietary services"
      ]
    },
    {
      "name": "evaluate-ip-risk",
      "description": "Assesses potential infringement exposure, licensing obligations, exclusivity constraints, and competitive risks.",
      "tags": ["riskAssessment", "infringementRisk", "licensing", "competitiveRisk"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "What risks arise from using this patented method",
        "Evaluate licensing obligations for this portfolio"
      ]
    },
    {
      "name": "trace-ip-provenance",
      "description": "Tracks ownership history, assignments, transfers, and corporate lineage of IP assets.",
      "tags": ["provenance", "ownership", "assignments", "corporateLineage"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "Who originally owned this patent",
        "Trace ownership changes for this portfolio"
      ]
    },
    {
      "name": "detect-related-ip",
      "description": "Identifies similar, adjacent, or competing IP assets across the market.",
      "tags": ["relatedPatents", "competitiveLandscape", "similaritySearch"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "Find patents similar to US-XXXXXXX",
        "Identify competing IP in this domain"
      ]
    },
    {
      "name": "simulate-ip-application",
      "description": "Models hypothetical product or service implementations using the entity’s IP to reveal potential commercial strategies.",
      "tags": ["simulation", "innovation", "productStrategy"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json", "text/plain"],
      "examples": [
        "Simulate how this patent could be used in a mobile app",
        "Model a service that uses these three patents together"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}