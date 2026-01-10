/**
 * This Tech-Inspector AuthenticatedExtendedCard conveys:
 * - AuthenticatedExtendedCard contains tasks, messages, tools, and artifacts for Registered Agents
 * - Tasks: A task encapsulates the entire interaction related to a specific goal or request.
 * - Messages: Messages are used for instructions, prompts, replies, and status updates.
 * - Artifacts: Collection of artifacts created by the agent.
 */

/**
* Tech-Inspector Authenticated Extended Agent Card¶
*/
{
  "name": "Tech-Inspector",
  "description": "Discovers technology vendors of a specific organization.",
  "url": "https://privacyportfolio.com/agent-registry/tech-inspector/auth/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
    },
  "iconUrl": "https://privacyportfolio.com/agent-registry/tech-inspector/tech-inspector-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/tech-inspector/auth/v1-Tech-Inspector-AuthenticatedExtendedAgentCard.md",
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
  "x-tools": [
    {
      "name": "integration-scanner",
      "description": "Searches systems, documentation, and codebases for references to third-party assets."
    },
    {
      "name": "portfolio-clustering-engine",
      "description": "Clusters third-party assets into technical and operational categories."
    },
    {
      "name": "provenance-tracker",
      "description": "Resolves version history, vendor lineage, and update provenance for third-party assets."
    }
  ],
  "x-messages": [
    {
      "name": "tech-discovery-complete",
      "description": "Signals that third-party asset discovery and integration mapping have completed."
    },
    {
      "name": "tech-report-ready",
      "description": "Push notification when a technical integration report has been generated."
    }
  ],
  "x-artifacts": [
    {
      "name": "asset-portfolio",
      "description": "Structured list of discovered third-party assets with metadata and provenance.",
      "content_type": "application/json"
    },
    {
      "name": "integration-map",
      "description": "Mapping of third-party assets to systems, workflows, and technical domains.",
      "content_type": "application/json"
    },
    {
      "name": "tech-report",
      "description": "Human-readable and machine-readable report summarizing third-party assets, integrations, risks, and technical impact.",
      "content_type": "application/json"
    },
    {
      "name": "evidence-manifest",
      "description": "Cryptographically signed manifest of discovery results, integration mappings, and risk evaluations.",
      "content_type": "application/json"
    }
  ],
 "supportsAuthenticatedExtendedCard": true
}