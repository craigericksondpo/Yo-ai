/**
 * This Door-Keeper AuthenticatedExtendedCard conveys:
 * - AuthenticatedExtendedCard contains tasks and messages for Registered Agents
 * - Tasks: A task encapsulates the entire interaction related to a specific goal or request.
 * - Messages: Messages are used for instructions, prompts, replies, and status updates.
 * - Artifacts: Collection of artifacts created by the agent.
 */


/**
* Door-Keeper Authenticated Extended Agent Card¶
*/
{
  "name": "Door-Keeper",
  "description": "Profiles guests and decides who to allow in and for what purpose.",
  "url": "https://privacyportfolio.com/agent-registry/door-keeper/auth/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://www.PrivacyPortfolio.com"
    },
  "iconUrl": "https://privacyportfolio.com/agent-registry/door-keeper/door-keeper-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/auth/v1-Door-Keeper-AuthenticatedExtendedAgentCard.md",
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
      "id": "identify-Visitor",
      "name": "identify-Visitor",
      "description": "Identify platform users and activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "identifier": { "type": "string" },
          "identifier_ref": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["log_refs", "identifier_ref", "identifier"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "identifier_ref": { "type": "string" },
          "finding": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    {
      "id": "register-Agent",
      "name": "register-Agent",
      "description": "Generates a RegisteredAgent card for qualified agents.",
      "tags": ["registered-agent", "denied-agent", "pending-registration"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "identifier_ref": { "type": "string" },
          "subscriber_ref": { "type": "string" },
          "org_ref": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["identifier_ref", "subscriber_ref", "log_refs"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "finding": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    {
      "id": "register-Subscriber",
      "name": "register-Subscriber",
      "description": "Generates a RegisteredSubscriber card for qualified subscribers.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "identifier": { "type": "string" },
          "identifier_ref": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["identifier", "identifier_ref", "log_refs"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "finding": { "type": "string" }
        }
      }
    },
    {
      "id": "authenticate-Agent",
      "name": "authenticate-Agent",
      "description": "Authenticate agents and monitor activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["registration_identifier_ref", "log_refs"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "finding": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    {
      "id": "authenticate-Subscriber",
      "name": "authenticate-Subscriber",
      "description": "Authenticate subscribers and monitor activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["registration_identifier_ref", "log_refs"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "finding": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    {
      "id": "generate-Credentials",
      "name": "generate-Credentials",
      "description": "Generates credentials for RegisteredAgents and RegisteredSubscribers.",
      "tags": ["RegisteredAgent", "RegisteredSubscriber", "Visitor"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["registration_identifier_ref", "log_refs"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "finding": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
    {
      "id": "manage-AccessRights",
      "name": "manage-AccessRights",
      "description": "Manage access rights for RegisteredAgents and RegisteredSubscribers.",
      "tags": ["RegisteredAgent", "RegisteredSubscriber", "Visitor"],
      "inputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["registration_identifier_ref", "log_refs"]
      },
      "outputSchema": {
        "type": "object",
        "properties": {
          "registration_identifier_ref": { "type": "string" },
          "finding": { "type": "string" },
          "log_refs": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      }
    },
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