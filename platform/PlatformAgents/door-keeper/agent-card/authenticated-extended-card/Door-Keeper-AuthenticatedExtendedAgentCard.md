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
  "documentationUrl": "https://privacyportfolio.com/agent-registry/auth/Door-Keeper-AuthenticatedExtendedAgentCard.md",
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
    {"name": "Agent.Authenticate"},
    {"name": "API.Validate"},
    {"name": "Trust.Assign"},
    {"name": "Visitor.Identify"},
    {"name": "Agent.Register"},
    {"name": "Subscriber.Register"},
    {"name": "Subscriber.Authenticate"},
    {"name": "Credentials.Generate"},
    {"name": "AccessRights.Manage"}
    ],
    "x-capabilities": [
        {
          "Agent.Authenticate": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "Agent.Authenticate"}},
                  {"artifact": {"type": "task", "name": "Agent.Authenticate"}},
                  {"artifact": {"type": "tool", "name": "Agent.Authenticate"}},
                  {"artifact": {"type": "handler", "name": "Agent.Authenticate"}},
                  {"artifact": {"type": "messageType", "name": "Agent.Authenticate.Input"}},
                  {"artifact": {"type": "messageType", "name": "Agent.Authenticate.Output"}}
              ]
          }
        },
        {
          "API.Validate": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "API.Validate"}},
                  {"artifact": {"type": "task", "name": "API.Validate"}},
                  {"artifact": {"type": "tool", "name": "API.Validate"}},
                  {"artifact": {"type": "handler", "name": "API.Validate"}},
                  {"artifact": {"type": "messageType", "name": "API.Validate.Input"}},
                  {"artifact": {"type": "messageType", "name": "API.Validate.Output"}}
              ]
          }
        },
        {
          "Trust.Assign": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "Trust.Assign"}},
                  {"artifact": {"type": "task", "name": "Trust.Assign"}},
                  {"artifact": {"type": "tool", "name": "Trust.Assign"}},
                  {"artifact": {"type": "handler", "name": "Trust.Assign"}},
                  {"artifact": {"type": "messageType", "name": "Trust.Assign.Input"}},
                  {"artifact": {"type": "messageType", "name": "Trust.Assign.Output"}}
              ]
          }
        },
        {
          "Visitor.Identify": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "Visitor.Identify"}},
                  {"artifact": {"type": "task", "name": "Visitor.Identify"}},
                  {"artifact": {"type": "tool", "name": "Visitor.Identify"}},
                  {"artifact": {"type": "handler", "name": "Visitor.Identify"}},
                  {"artifact": {"type": "messageType", "name": "Visitor.Identify.Input"}},
                  {"artifact": {"type": "messageType", "name": "Visitor.Identify.Output"}}
              ]
          }
        },
        {
          "Agent.Register": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "Agent.Register"}},
                  {"artifact": {"type": "task", "name": "Agent.Register"}},
                  {"artifact": {"type": "tool", "name": "Agent.Register"}},
                  {"artifact": {"type": "handler", "name": "Agent.Register"}},
                  {"artifact": {"type": "messageType", "name": "Agent.Register.Input"}},
                  {"artifact": {"type": "messageType", "name": "Agent.Register.Output"}}
              ]
          }
        },
        {
          "Subscriber.Register": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "Subscriber.Register"}},
                  {"artifact": {"type": "task", "name": "Subscriber.Register"}},
                  {"artifact": {"type": "tool", "name": "Subscriber.Register"}},
                  {"artifact": {"type": "handler", "name": "Subscriber.Register"}},
                  {"artifact": {"type": "messageType", "name": "Subscriber.Register.Input"}},
                  {"artifact": {"type": "messageType", "name": "Subscriber.Register.Output"}}
              ]
          }
        },
        {
          "Subscriber.Authenticate": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "Subscriber.Authenticate"}},
                  {"artifact": {"type": "task", "name": "Subscriber.Authenticate"}},
                  {"artifact": {"type": "tool", "name": "Subscriber.Authenticate"}},
                  {"artifact": {"type": "handler", "name": "Subscriber.Authenticate"}},
                  {"artifact": {"type": "messageType", "name": "Subscriber.Authenticate.Input"}},
                  {"artifact": {"type": "messageType", "name": "Subscriber.Authenticate.Output"}}
              ]
          }
        },
        {
          "Credentials.Generate": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "Credentials.Generate"}},
                  {"artifact": {"type": "task", "name": "Credentials.Generate"}},
                  {"artifact": {"type": "tool", "name": "Credentials.Generate"}},
                  {"artifact": {"type": "handler", "name": "Credentials.Generate"}},
                  {"artifact": {"type": "messageType", "name": "Credentials.Generate.Input"}},
                  {"artifact": {"type": "messageType", "name": "Credentials.Generate.Output"}}
              ]
          }
        },
        {
          "AccessRights.Manage": {
              "artifacts": [
                  {"artifact": {"type": "skill", "name": "AccessRights.Manage"}},
                  {"artifact": {"type": "task", "name": "AccessRights.Manage"}},
                  {"artifact": {"type": "tool", "name": "AccessRights.Manage"}},
                  {"artifact": {"type": "handler", "name": "AccessRights.Manage"}},
                  {"artifact": {"type": "messageType", "name": "AccessRights.Manage.Input"}},
                  {"artifact": {"type": "messageType", "name": "AccessRights.Manage.Output"}}
              ]
          }
        }
    ],
  "x-artifacts": [
    {
      "name": "Agent.Authenticate",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Authenticate agents and monitor activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"]
    },
    {
      "name": "Agent.Authenticate",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Authenticate agents and monitor activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"]
    },
    {
      "name": "Agent.Authenticate",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Requests access and receives response.",
      "path": "/authentication-claim.py",
      "capabilities": ["authenticate"],
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "AgentAuthenticator",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/Agent.Authenticate.html",
        "config": {
          "backend": "AWS Cognito"
        }
      },
      "inputSchema": { "$ref": "#/schemas/Agent.Authenticate.Input" },
      "outputSchema": { "$ref": "#/schemas/Agent.Authenticate.Output" },
      "auth": "apiKey"
    },
    {
      "name": "AgentCardValidator",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Validates agent cards and subscriber identities",
      "path": "/validator.py",
      "capabilities": ["validate"],
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "AgentCardValidator",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/AgentCardValidator.html",
        "config": {}
      },
      "inputSchema": { "$ref": "#/schemas/AgentCardValidator.Input" },
      "outputSchema": { "$ref": "#/schemas/AgentCardValidator.Output" },
      "auth": "apiKey"
    },
    {
      "name": "Agent.Authenticate",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/authentication-claim-handler.py"
    },
    {
      "name": "Agent.Authenticate.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Agent.Authenticate#/definitions/Input" },
      "description": "Input schema for authenticating agent."
    },
    {
      "name": "Agent.Authenticate.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Agent.Authenticate#/definitions/Output" },
      "description": "Output schema for authenticating agent."
    },
    {
      "name": "API.Validate",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Validates API access and emits an ApiAccessValidated event.",
      "tags": [""]
    },
    {
      "name": "API.Validate",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Validates API access and emits an ApiAccessValidated event.",
      "tags": [""]
    },
    {
      "name": "API.Validate",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Validates API access and emits an ApiAccessValidated event.",
      "capabilities": ["validate"],
      "path": "/",
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/API.Validate.html",
        "config": {
          "backend": ""
        }
      },
      "inputSchema": { "$ref": "#/schemas/API.Validate.Input" },
      "outputSchema": { "$ref": "#/schemas/API.Validate.Output" },
      "auth": "apiKey"
    },
    {
      "name": "API.Validate",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/"
    },
    {
      "name": "API.Validate.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/API.Validate#/definitions/Input" },
      "description": "Input schema for API access validation."
    },
    {
      "name": "API.Validate.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/API.Validate#/definitions/Output" },
      "description": "Output schema for API access validation."
    },
    {
      "name": "Trust.Assign",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Assigns a trust tier to a visitor and emits VisitorTrustTierAssigned.",
      "tags": [""]
    },
    {
      "name": "Trust.Assign",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Assigns a trust tier to a visitor and emits VisitorTrustTierAssigned.",
      "tags": [""]
    },
    {
      "name": "Trust.Assign",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Assigns a trust tier to a visitor and emits VisitorTrustTierAssigned.",
      "capabilities": ["evaluate"],
      "path": "",
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/Trust.Assign.html",
        "config": {
          "backend": ""
        }
      },
      "inputSchema": { "$ref": "#/schemas/Trust.Assign.Input" },
      "outputSchema": { "$ref": "#/schemas/Trust.Assign.Output" },
      "auth": "apiKey"
    },
    {
      "name": "Trust.Assign",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/"
    },
    {
      "name": "Trust.Assign.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Trust.Assign#/definitions/Input" },
      "description": "Input schema for trust tier assignment."
    },
    {
      "name": "Trust.Assign.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Trust.Assign#/definitions/Output" },
      "description": "Output schema for trust tier assignment."
    },
    {
      "name": "Visitor.Identify",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Identify platform users and activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"]
    },
    {
      "name": "Visitor.Identify",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Identify platform users and activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"]
    },
    {
      "name": "Visitor.Identify",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Identify platform users and activity.",
      "capabilities": ["identify"],
      "path": "/",
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/Visitor.Identify.html",
        "config": {
          "backend": ""
        }
      },
      "inputSchema": { "$ref": "#/schemas/Visitor.Identify.Input" },
      "outputSchema": { "$ref": "#/schemas/Visitor.Identify.Output" },
      "auth": "apiKey"
    },
    {
      "name": "Visitor.Identify",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/"
    },
    {
      "name": "Visitor.Identify.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Visitor.Identify#/definitions/Input" },
      "description": "Input schema for ."
    },
    {
      "name": "Visitor.Identify.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Visitor.Identify#/definitions/Output" },
      "description": "Output schema for ."
    },
    {
      "name": "Agent.Register",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Generates a RegisteredAgent card for qualified agents.",
      "tags": ["registered-agent", "denied-agent", "pending-registration"]
    },
    {
      "name": "Agent.Register",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Generates a RegisteredAgent card for qualified agents.",
      "tags": ["registered-agent", "denied-agent", "pending-registration"]
    },
    {
      "name": "Agent.Register",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Generates a RegisteredAgent card for qualified agents.",
      "capabilities": ["register"],
      "path": "/",
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/Agent.Register.html",
        "config": {
          "backend": ""
        }
      },
      "inputSchema": { "$ref": "#/schemas/Agent.Register.Input" },
      "outputSchema": { "$ref": "#/schemas/Agent.Register.Output" },
      "auth": "apiKey"
    },
    {
      "name": "Agent.Register",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/"
    },
    {
      "name": "Agent.Register.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Agent.Register#/definitions/Input" },
      "description": "Input schema for ."
    },
    {
      "name": "Agent.Register.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Agent.Register#/definitions/Output" },
      "description": "Output schema for ."
    },
    {
      "name": "Subscriber.Register",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Generates a RegisteredSubscriber card for qualified subscribers.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"]
    },
    {
      "name": "Subscriber.Register",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Generates a RegisteredSubscriber card for qualified subscribers.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"]
    },
    {
      "name": "Subscriber.Register",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Generates a RegisteredSubscriber card for qualified subscribers.",
      "capabilities": ["register"],
      "path": "/",
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/Subscriber.Register.html",
        "config": {
          "backend": ""
        }
      },
      "inputSchema": { "$ref": "#/schemas/Subscriber.Register.Input" },
      "outputSchema": { "$ref": "#/schemas/Subscriber.Register.Output" },
      "auth": "apiKey"
    },
    {
      "name": "Subscriber.Register",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/"
    },
    {
      "name": "Subscriber.Register.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Subscriber.Register#/definitions/Input" },
      "description": "Input schema for ."
    },
    {
      "name": "Subscriber.Register.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Subscriber.Register#/definitions/Output" },
      "description": "Output schema for ."
    },
    {
      "name": "Subscriber.Authenticate",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Authenticate subscribers and monitor activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"]
    },
    {
      "name": "Subscriber.Authenticate",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Authenticate subscribers and monitor activity.",
      "tags": ["decision-event", "decision-factor", "decision-outcome"]
    },
    {
      "name": "Subscriber.Authenticate",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Authenticate subscribers and monitor activity.",
      "capabilities": ["authenticate"],
      "path": "/",
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/Subscriber.Authenticate.html",
        "config": {
          "backend": ""
        }
      },
      "inputSchema": { "$ref": "#/schemas/Subscriber.Authenticate.Input" },
      "outputSchema": { "$ref": "#/schemas/Subscriber.Authenticate.Output" },
      "auth": "apiKey"
    },
    {
      "name": "Subscriber.Authenticate",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/"
    },
    {
      "name": "Subscriber.Authenticate.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Subscriber.Authenticate#/definitions/Input" },
      "description": "Input schema for ."
    },
    {
      "name": "Subscriber.Authenticate.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Subscriber.Authenticate#/definitions/Output" },
      "description": "Output schema for ."
    },
    {
      "name": "Credentials.Generate",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Generates credentials for RegisteredAgents and RegisteredSubscribers.",
      "tags": ["RegisteredAgent", "RegisteredSubscriber", "Visitor"]
    },
    {
      "name": "Credentials.Generate",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Generates credentials for RegisteredAgents and RegisteredSubscribers.",
      "tags": ["RegisteredAgent", "RegisteredSubscriber", "Visitor"]
    },
    {
      "name": "Credentials.Generate",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Generates credentials for RegisteredAgents and RegisteredSubscribers.",
      "capabilities": ["generate"],
      "path": "/",
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/Credentials.Generate.html",
        "config": {
          "backend": ""
        }
      },
      "inputSchema": { "$ref": "#/schemas/Credentials.Generate.Input" },
      "outputSchema": { "$ref": "#/schemas/Credentials.Generate.Output" },
      "auth": "apiKey"
    },
    {
      "name": "Credentials.Generate",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/"
    },
    {
      "name": "Credentials.Generate.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Credentials.Generate#/definitions/Input" },
      "description": "Input schema for ."
    },
    {
      "name": "Credentials.Generate.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/Credentials.Generate#/definitions/Output" },
      "description": "Output schema for ."
    },
    {
      "name": "AccessRights.Manage",
      "version": "1.0.0",
      "artifactType": "skill",
      "description": "Manage access rights for RegisteredAgents and RegisteredSubscribers.",
      "tags": ["RegisteredAgent", "RegisteredSubscriber", "Visitor"]
    },
    {
      "name": "AccessRights.Manage",
      "version": "1.0.0",
      "artifactType": "task",
      "description": "Manage access rights for RegisteredAgents and RegisteredSubscribers.",
      "tags": ["RegisteredAgent", "RegisteredSubscriber", "Visitor"]
    },
    {
      "name": "AccessRights.Manage",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Manage access rights for RegisteredAgents and RegisteredSubscribers.",
      "capabilities": ["manage"],
      "path": "/",
      "provider": {
        "name": "PrivacyPortfolio",
        "brand": "Yo-ai",
        "product": "",
        "version": "1.0.0",
        "license": "Yo-ai Internal",
        "url": "https://yo-ai.ai/docs/AccessRights.Manage.html",
        "config": {
          "backend": ""
        }
      },
      "inputSchema": { "$ref": "#/schemas/AccessRights.Manage.Input" },
      "outputSchema": { "$ref": "#/schemas/AccessRights.Manage.Output" },
      "auth": "apiKey"
    },
    {
      "name": "AccessAdministrator",
      "version": "1.0.0",
      "artifactType": "tool",
      "description": "Administers Kafka and external tool access rights and issues credentials.",
      "capabilities": ["grant", "revoke", "issue-credentials"],
      "path": "/access_admin.py",
      "provider": {
        "name": "Apache",
        "brand": "Apache",
        "product": "Kafka",
        "version": "3.7.0",
        "license": "Apache-2.0",
        "url": "https://kafka.apache.org",
        "config": {
          "bootstrapServers": "kafka:9092",
          "securityProtocol": "SASL_SSL"
        }
      },
      "inputSchema": { "$ref": "#/schemas/AccessRights.Manage.Input" },
      "outputSchema": { "$ref": "#/schemas/AccessRights.Manage.Output" },
      "auth": "apiKey"
    },
    {
      "name": "AccessRights.Manage",
      "version": "1.0.0",
      "artifactType": "handler",
      "description": "Interface for integrating with tool executable.",
      "path": "/"
    },
    {
      "name": "AccessRights.Manage.Input",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/AccessRights.Manage#/definitions/Input" },
      "description": "Input schema for ."
    },
    {
      "name": "AccessRights.Manage.Output",
      "version": "1.0.0",
      "artifactType": "messageType",
      "schema": { "$ref": "#/schemas/AccessRights.Manage#/definitions/Output" },
      "description": "Output schema for ."
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}
