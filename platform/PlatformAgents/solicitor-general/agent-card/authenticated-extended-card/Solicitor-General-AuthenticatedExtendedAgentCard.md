/**
 * This Solicitor-General AuthenticatedExtendedCard conveys:
 * - AuthenticatedExtendedCard contains tasks, messages, tools, and artifacts for Registered Agents
 * - Tasks: A task encapsulates the entire interaction related to a specific goal or request.
 * - Messages: Messages are used for instructions, prompts, replies, and status updates.
 * - Artifacts: Collection of artifacts created by the agent.
 */

/**
* Solicitor-General Authenticated Extended AgentCard¶
*/
{
    "name": "Solicitor-General",
    "description": "Root Agent that logs all platform events, manages tasks and storage, and correlates requests with responses for routing.",
    "url": "https://privacyportfolio.com/agent-registry/solicitor-general/auth/agent.json",
    "provider": {
        "organization": "PrivacyPortfolio",
        "url": "https://privacyportfolio.com"
    },
    "iconUrl": "https://privacyportfolio.com/agent-registry/solicitor-general/solicitor-general-agent-icon.png",
    "version": "1.0.0",
    "documentationUrl": "https://privacyportfolio.com/agent-registry/solicitor-general/auth/Solicitor-General-AuthenticatedExtendedAgentCard.md",
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
        {"name": "Event.Log"},
        {"name": "Request-Response.Correlate"}
    ],
    "x-capabilities": [
        {
            "Event.Log": {
                "artifacts": [
                    {"artifact": {"type": "skill", "name": "Event.Log"}},
                    {"artifact": {"type": "task", "name": "Event.Log"}},
                    {"artifact": {"type": "tool", "name": "Event.Log"}},
                    {"artifact": {"type": "handler", "name": "Event.Log"}},
                    {"artifact": {"type": "messageType", "name": "Event.Log.Input"}},
                    {"artifact": {"type": "messageType", "name": "Event.Log.Output"}}
                ]
            }
        },
        {
            "Request-Response.Correlate": {
                "artifacts": [
                    {"artifact": {"type": "skill", "name": "Request-Response.Correlate"}},
                    {"artifact": {"type": "task", "name": "Request-Response.Correlate"}},
                    {"artifact": {"type": "tool", "name": "Request-Response.Correlate"}},
                    {"artifact": {"type": "handler", "name": "Request-Response.Correlate"}},
                    {"artifact": {"type": "messageType", "name": "Request-Response.Correlate.Input"}},
                    {"artifact": {"type": "messageType", "name": "Request-Response.Correlate.Output"}}
                ]
            }
        }
    ],
    "x-artifacts": [
        {
        "name": "Event.Log",
        "version": "1.0.0",
        "artifactType": "skill",
        "description": "Inserts a record into the EventLog.",
        "tags": ["audit"],
        "examples": ["Log event"]
        },
        {
        "name": "Event.Log",
        "version": "1.0.0",
        "artifactType": "task",
        "description": "Inserts a record into the EventLog.",
        "tags": ["audit"],
        "examples": ["Log event"]
        },
        {
        "name": "Event.Log",
        "version": "1.0.0",
        "artifactType": "tool",
        "description": "Inserts a record into the EventLog.",
        "capabilities": ["log"],
        "path": "/",
        "provider": {
            "name": "PrivacyPortfolio",
            "brand": "Yo-ai",
            "product": "",
            "version": "1.0.0",
            "license": "Yo-ai Internal",
            "url": "https://yo-ai.ai/docs/Event.Log.html",
            "config": {
            "backend": ""
            }
        },
        "inputSchema": { "$ref": "#/schemas/Event.Log.Input" },
        "outputSchema": { "$ref": "#/schemas/Event.Log.Output" },
        "auth": "apiKey"
        },
        {
        "name": "Event.Log",
        "version": "1.0.0",
        "artifactType": "handler",
        "description": "Interface for integrating with tool executable.",
        "path": "/"
        },
        {
        "name": "Event.Log.Input",
        "version": "1.0.0",
        "artifactType": "messageType",
        "schema": { "$ref": "#/schemas/Event.Log#/definitions/Input" },
        "description": "Input schema for ."
        },
        {
        "name": "Event.Log.Output",
        "version": "1.0.0",
        "artifactType": "messageType",
        "schema": { "$ref": "#/schemas/Event.Log#/definitions/Output" },
        "description": "Output schema for ."
        },
        {
        "name": "Request-Response.Correlate",
        "version": "1.0.0",
        "artifactType": "skill",
        "description": "Agent that correlates responses with requests for routing.",
        "tags": ["logEntry", "topic", "request", "response"],
        "examples": [
            "Who responded to request [requestID] on topic [topicID].",
            "Who requested request [responseID] on topic [topicID]."
        ]
        },
        {
        "name": "Request-Response.Correlate",
        "version": "1.0.0",
        "artifactType": "task",
        "description": "Agent that correlates responses with requests for routing.",
        "tags": ["logEntry", "topic", "request", "response"]
        },
        {
        "name": "Request-Response.Correlate",
        "version": "1.0.0",
        "artifactType": "tool",
        "description": "Agent that correlates responses with requests for routing.",
        "capabilities": ["correlate"],
        "path": "/",
        "provider": {
            "name": "PrivacyPortfolio",
            "brand": "Yo-ai",
            "product": "",
            "version": "1.0.0",
            "license": "Yo-ai Internal",
            "url": "https://yo-ai.ai/docs/Request-Response.Correlate.html",
            "config": {
            "backend": ""
            }
        },
        "inputSchema": { "$ref": "#/schemas/Request-Response.Correlate.Input" },
        "outputSchema": { "$ref": "#/schemas/Request-Response.Correlate.Output" },
        "auth": "apiKey"
        },
        {
        "name": "Request-Response.Correlate",
        "version": "1.0.0",
        "artifactType": "handler",
        "description": "Interface for integrating with tool executable.",
        "path": "/"
        },
        {
        "name": "Request-Response.Correlate.Input",
        "version": "1.0.0",
        "artifactType": "messageType",
        "schema": { "$ref": "#/schemas/Request-Response.Correlate#/definitions/Input" },
        "description": "Input schema for ."
        },
        {
        "name": "Request-Response.Correlate.Output",
        "version": "1.0.0",
        "artifactType": "messageType",
        "schema": { "$ref": "#/schemas/Request-Response.Correlate#/definitions/Output" },
        "description": "Output schema for ."
        }
    ],
    "supportsAuthenticatedExtendedCard": true
}