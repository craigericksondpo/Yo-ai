/http/README.md

The /http folder defines the public HTTP interface layer for the Yo-ai Platform.

It contains:
•	the universal Lambda/HTTP entrypoint for all A2A and Starlette traffic
•	the OpenAPI-compatible handler for API Gateway and OpenAI-compatible clients
•	the OpenAPI specification describing all exposed HTTP endpoints
•	no business logic, no agent logic, and no platform runtime code

This layer is intentionally minimal and declarative.

Its purpose is to make the platform's HTTP surface:
•	explicit
•	versionable
•	auditable
•	stable for external developers
•	decoupled from internal agent logic
________________________________________
1. Folder Structure

/http
    __init__.py
    yo_ai_handler.py

    /openapi
        openapi.yaml
        api_handler.py
        __init__.py

________________________________________
2. yo_ai_handler.py — Universal Lambda / HTTP Entrypoint

This module is the front door for all agents on the platform. Every
request enters here regardless of which agent the caller addressed.

It handles two startup modes:

    Mode 1 — HTTP A2A (startup_mode="a2a")
        POST /a2a — inbound A2A v1.0 JSON-RPC envelope from any external
        caller. Delegates to A2ATransport → SolicitorGeneral.

    Mode 4 — Starlette/MCP (startup_mode="starlette")
        Starlette Request object passed directly — used by MCP clients
        and streaming consumers.

It also serves the platform's lightweight HTTP routes:

    GET /
        Plain-text landing page. Points callers to the Agent Directory
        URL and the A2A endpoint. No hardcoded agent card content.

    GET /.well-known/agent-card.json
        301 redirect to the canonical Agent Directory:
            https://privacyportfolio.com/.well-known/agent.json
        The agent card is maintained on the website — not in this
        codebase. Updating the website is the only deployment required.

    POST /register, /auth, /permissions
    GET  /agent/extended
        Return 501 Not Implemented. These endpoints are known and
        intentional — they will route through Door-Keeper capabilities
        (Agent.Register, Subscriber.Authenticate, AccessRights.Manage,
        showCard()) when implemented. 501 distinguishes "not yet wired"
        from "does not exist".

yo_ai_handler.py contains no business logic. All logic is delegated to:
•	/a2a (A2ATransport — envelope validation, correlation, taskId)
•	/agents/solicitor_general (routing, AGENT_REGISTRY, context assembly)
•	/core (runtime pipeline — schemas, knowledge, AI)
•	/shared (capability_map, tools, policies)

________________________________________
3. /openapi/api_handler.py — API Gateway / OpenAI-Compatible Handler

This module handles Mode 3 traffic (startup_mode="api"):

    Mode 3 — API Gateway / OpenAI-compatible (startup_mode="api")
        Receives requests from OpenAI-compatible API clients and AWS
        API Gateway. Maps URL path segments and request bodies to
        canonical capability IDs, then runs the same handler dispatch
        pipeline as Mode 1.

It handles two Lambda event shapes:

    Shape A — API Gateway HTTP API (v2 payload format)
        { "rawPath": "/agents/door-keeper/TrustAssign", "body": "..." }

    Shape B — Direct Lambda invocation
        { "capability": "Trust.Assign", "payload": { ... } }

Path segments follow the convention: capability ID with dots removed.
    Trust.Assign → /agents/door-keeper/TrustAssign

api_handler.py contains no business logic. All capability logic is
delegated to agent run() modules via CAPABILITY_DISPATCH.

________________________________________
4. /openapi/openapi.yaml — The API Contract

This file defines the entire external HTTP interface of the platform.

It includes:
•	endpoint paths
•	request/response schemas
•	authentication requirements
•	capability routing metadata
•	error formats
•	versioning and metadata

openapi.yaml is the single source of truth for:
•	API documentation
•	client SDK generation
•	integration testing
•	external developer onboarding

No HTTP endpoint should exist unless it is declared here.

________________________________________
5. Design Principles

- Declarative, not imperative
  The HTTP layer describes what the API looks like, not how it works.

- Single source of truth
  openapi.yaml defines the platform's public contract.
  The Agent Directory (privacyportfolio.com/.well-known/agent.json)
  is the single source of truth for the agent card — not this codebase.

- No business logic
  All logic lives in the agent runtime and capability handlers.

- Audit friendly
  The HTTP layer is small, explicit, and easy to diff.

- Stable for external developers
  Changes to the HTTP surface must be intentional and versioned.

________________________________________
6. How the HTTP Layer Fits Into the Platform

The execution flow is:

    Mode 1 / Mode 4 (A2A and Starlette):
    1.  Client → POST /a2a or Starlette request
    2.  yo_ai_handler.py → A2ATransport.handle_a2a()
    3.  A2ATransport → SolicitorGeneral.route()
    4.  SolicitorGeneral → agent handler (local) or Lambda (remote)
    5.  agent handler → run(payload, agent_ctx, capability_ctx)
    6.  response → shaped + validated → returned to client

    Mode 3 (API Gateway / OpenAI-compatible):
    1.  Client → API Gateway → Lambda
    2.  api_handler.py → CAPABILITY_DISPATCH[capability_id]
    3.  agent method → run(payload, agent_ctx, capability_ctx)
    4.  response → shaped + validated → returned to client

The /http folder is responsible only for steps 1 and 2 in each path.

________________________________________
7. When to Modify This Folder

Modify /http when:
•	adding a new public endpoint
•	changing request/response schemas
•	updating authentication requirements
•	versioning or deprecating API paths
•	exposing new capabilities via HTTP
•	wiring a stub endpoint (501) to its Door-Keeper capability

Do not modify this folder when:
•	adding new agents
•	changing agent logic
•	updating internal schemas
•	modifying runtime behavior
•	changing capability routing
•	updating the agent card — edit the Agent Directory on the website
________________________________________
