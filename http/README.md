/http/README.md

The /http folder defines the public HTTP interface layer for the Yo ai Platform.

It contains:
•	the OpenAPI specification describing all exposed HTTP endpoints
•	the route binding layer that maps HTTP paths to capability execution
•	no business logic, no agent logic, and no platform runtime code

This layer is intentionally minimal and declarative.

Its purpose is to make the platform’s HTTP surface:
•	explicit
•	versionable
•	auditable
•	stable for external developers
•	decoupled from internal agent logic
________________________________________
1. Folder Structure

/http
    __init__.py

    /openapi
        openapi.yaml
        __init__.py

    /routes
        http_router.py
        __init__.py

________________________________________
2. /openapi/openapi.yaml — The API Contract

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
3. /routes/http_router.py — Route Binding Layer

This module binds HTTP paths to platform capabilities.

It is responsible for:
•	loading the OpenAPI specification
•	mapping each path to a handler
•	delegating execution to the capability router
•	enforcing request/response schema validation
•	applying platform level middleware (auth, logging, etc.)

It contains no business logic.
All logic is delegated to:
•	/core (runtime pipeline)
•	/agents (capability handlers)
•	/a2a (cross agent messaging)
•	/shared (schemas, tools, policies)

The router is intentionally thin to prevent drift and ensure that:
•	HTTP behavior is predictable
•	capability routing is centralized
•	the API surface remains stable
________________________________________
4. Design Principles

- Declarative, not imperative
- The HTTP layer describes what the API looks like, not how it works.
- Single source of truth
- openapi.yaml defines the platform’s public contract.
- No business logic
- All logic lives in the agent runtime and capability handlers.
- Audit friendly
- The HTTP layer is small, explicit, and easy to diff.
- Stable for external developers

Changes to the HTTP surface must be intentional and versioned.
________________________________________
5. How the HTTP Layer Fits Into the Platform

The execution flow is:
1.	Client → HTTP endpoint
2.	http_router.py → capability_router.py
3.	capability_router.py → agent handler
4.	agent handler → core runtime pipeline
5.	runtime → AI provider / knowledge / schemas
6.	response → shaped + validated → returned to client

The /http folder is responsible only for steps 1 and part of 2.
________________________________________
6. When to Modify This Folder

Modify /http when:
•	adding a new public endpoint
•	changing request/response schemas
•	updating authentication requirements
•	versioning or deprecating API paths
•	exposing new capabilities via HTTP

Do not modify this folder when:
•	adding new agents
•	changing agent logic
•	updating internal schemas
•	modifying runtime behavior
•	changing capability routing
________________________________________
