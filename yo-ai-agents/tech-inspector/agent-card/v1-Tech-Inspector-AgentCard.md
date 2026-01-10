/**
 * This Tech-Inspector AgentCard conveys:
 * - Overall details (version, name, description, uses)
 * - Skills: A set of capabilities the agent can perform
 * - Default modalities/content types supported by the agent.
 * - Authentication requirements
 * - AuthenticatedExtendedCard contains tasks and messages for Registered Agents
 */

/**
* Tech-Inspector AgentCard¶
*/
{
  "name": "Tech-Inspector",
  "description": "Discovers technology vendors of a specific organization.",
  "url": "https://privacyportfolio.com/agent-registry/tech-inspector/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
    },
  "iconUrl": "https://privacyportfolio.com/agent-registry/tech-inspector/tech-inspector-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/tech-inspector/v1-Tech-Inspector-AgentCard.md",
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
      "name": "discover-third-party-assets",
      "description": "Identifies third-party technologies, services, SDKs, APIs, data feeds, modules, and vendor-provided assets used by an organization.",
      "tags": ["thirdParty", "assetDiscovery", "vendorTech", "integrationInventory"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "List all third-party technologies used by Vendor X",
        "Discover external services integrated into this product"
      ]
    },
    {
      "name": "map-asset-integrations",
      "description": "Determines how third-party assets are integrated into organizational systems, workflows, data flows, and technical domains.",
      "tags": ["integrationMapping", "systemArchitecture", "dependencyAnalysis"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "How is this third-party service integrated into our workflow",
        "Map integrations for this vendor-provided SDK"
      ]
    },
    {
      "name": "analyze-implementation-details",
      "description": "Examines implementation patterns, configuration, data flows, and operational dependencies of third-party assets.",
      "tags": ["implementationAnalysis", "configuration", "dataFlow", "technicalAssessment"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Analyze how this API is implemented",
        "Review configuration and data flow for this integration"
      ]
    },
    {
      "name": "search-usage-instances",
      "description": "Searches for real-world usage instances of third-party assets across systems, documentation, codebases, and operational artifacts.",
      "tags": ["usageDiscovery", "techDiscovery", "integrationSearch"],
      "input_modes": ["application/json", "text/plain"],
      "output_modes": ["application/json"],
      "examples": [
        "Where is this SDK used in our environment",
        "Find all systems that rely on this vendor service"
      ]
    },
    {
      "name": "infer-technical-impact",
      "description": "Infers the operational, architectural, and compliance impact of integrating a third-party asset.",
      "tags": ["impactAnalysis", "architecture", "riskAssessment", "technicalDependencies"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json", "text/plain"],
      "examples": [
        "What is the technical impact of using this vendor service",
        "Infer risks and dependencies for this integration"
      ]
    },
    {
      "name": "cluster-asset-portfolio",
      "description": "Groups third-party assets into categories such as infrastructure, analytics, identity, data processing, or operational tooling.",
      "tags": ["portfolioClustering", "taxonomy", "classification", "techDomains"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Cluster all third-party assets used by this vendor",
        "Group integrations by technical domain"
      ]
    },
    {
      "name": "evaluate-integration-risk",
      "description": "Assesses security, privacy, operational, and compliance risks associated with third-party integrations.",
      "tags": ["riskAssessment", "security", "privacy", "operationalRisk"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Evaluate risk for integrating this external service",
        "Assess compliance impact of this third-party SDK"
      ]
    },
    {
      "name": "trace-integration-provenance",
      "description": "Tracks the origin, version history, update lineage, and vendor changes for third-party assets.",
      "tags": ["provenance", "versioning", "vendorLineage"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Trace provenance for this SDK",
        "Show version history and vendor changes"
      ]
    },
    {
      "name": "detect-related-assets",
      "description": "Identifies similar or alternative third-party assets across the market, including competing or complementary technologies.",
      "tags": ["competitiveLandscape", "similaritySearch", "alternatives"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json"],
      "examples": [
        "Find alternatives to this vendor service",
        "Identify similar SDKs in this domain"
      ]
    },
    {
      "name": "generate-tech-report",
      "description": "Produces a structured, regulator-friendly report summarizing discovered assets, integrations, risks, and technical impact.",
      "tags": ["reporting", "audit", "documentation", "evidence"],
      "input_modes": ["application/json"],
      "output_modes": ["application/json", "text/plain"],
      "examples": [
        "Generate a tech integration report for Vendor X",
        "Create a summary of all third-party assets used in this system"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}