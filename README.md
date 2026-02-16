# Yo-ai: AI Assurance Platform for Consumers and Organizations

Yo-ai is an AI Assurance Platform that enables Consumers and Organizations to establish secure, transparent, and mutually governed A2A (Agent to Agent) communication channels.
The Consumer is represented by the Data-Steward, an AI Agent that makes decisions and acts on the Consumer's behalf. 
The Organization is represented by the Vendor-Manager, and AI Agent that acts as a proxy to represent the organization.

Both sides use profiles to represent individual persons and corporate entities. These profiles are loaded, referenced, and updated by a team of cooperating AI Agents that can communicate:
- directly with the real-world parties they represent, or
- through A2A interchanges operatating inside isolated internal sandboxes.

Real people use Yo-ai to interact with each other's agents when they are unavailable or unknown to each other.
This drastically reduces latency in all processes, while also providing security, accountability, and privacy.

## What Yo-ai Enables
Yo-ai provides a structured way for individuals and organizations to:

-	Open A2A communication channels
-	Negotiate mutually agreed-upon data processing agreements
-	Train each other’s AI Agents to “play well with others”
-	Test for impacts to the corresponding party before, during, or after changes in processing
-	Build trust through transparency, primarily by sharing event logs about their agents’ activities

## Who the Yo-ai Platform Serves
Everyone who wants something, and anyone who cannot be everywhere all at once.

## Problems the Yo-ai Platform Solves
-		Distrust. ”Who comes knocking at my door? What are doing? What do you want? How can I engage with you – or not?”
-		High-latency processes. “My agent can produce this now. When can you get back to me?”

## Benefits the Yo-ai Platform Provides
As an evidence-based learning system for autonomous decision-making, Yo-ai provides 'explainability' through log-shipping for a unified system of truth for all participants in a process.  

# **How This Repository Is Structured**
Yo‑ai is a multi-agent, federated platform of FastA2A agents that can be cloned and run within any environment. 
A Makefile documents which modules are importable as Python packages.
Every top‑level directory contains a README.md.

### **`/core`**
 Summary: 
 Foundational agent classes and shared abstractions.
 
 Usage:
 Importable Python packages for agent class definitions.
 All platform agents inherit from these classes.

 Contains: 
 - Agent — base class for all agents
 - PlatformAgent — privileged platform‑side agent
 - YoAiAgent — consumer/organization‑side agent
 - AgentCard-Architecture.docx — architectural reference for agent cards

### **`/a2a`**
 Summary:
 Shared FastA2A runtime and the glue layer between Starlette and the Solicitor‑General.

 Usage:
 Imported by the Starlette app to mount the A2A runtime under /a2a/*.
 This is the primary machine‑facing entrypoint for A2A JSON‑RPC requests.

 Contains:
 - app.py — shared FastA2A runtime instance
 - handlers.py — A2A HTTP handler bridging Starlette ↔ FastA2A ↔ Solicitor‑General
 - routes_a2a.py — public A2A endpoint that receives JSON‑RPC requests and forwards them to the Solicitor‑General


### **`/app`**
 Summary:
 Top‑level Starlette application and platform bootstrap.
 
 Usage:
 Executed as the main application entrypoint.
 Initializes the Solicitor‑General, mounts A2A routes, and configures middleware.

 Contains:
 - main.py — Starlette app + FastA2A mounts + Solicitor‑General bootstrap
 - dependencies.py — external service wiring
 - config.py — environment variables, settings, logfire configuration
 - /middleware/ — authentication, logging, and error‑handling middleware

### **`/http`**
 Summary:
 HTTP‑facing routes, OpenAPI specification.

 Usage:
 Imported by the Starlette app to expose public HTTP routes for agents and A2A operations.
 
 Contains:
 - /routes/http_router.py — public A2A JSON‑RPC endpoint
 - /routes/agent_routes.py — agent‑specific invocation routes (/agent/{id}/invoke)
 - /openapi/openapi.yaml — Yo‑API capability definitions

### **`/agents`**
 Summary:
 Standalone agent bundles for consumer‑side and organization‑side teams.

 Usage:
 Each folder represents a complete agent package, including identity, capabilities, training materials, and artifacts.

 Contains:
 - agent.json — identity + capabilities
 - Agent card documentation
 - Training manuals
 - Artifacts (schemas, agreements, policies, knowledge)
 - Chat transcripts used to develop each agent

### **`/shared`**
 Summary:
 Shared resources used across all Yo‑ai agents.

 Usage:
 Imported by agents and platform components to ensure consistent schemas, policies, and tools.

 Contains:
 /artifacts
 - Subscriber and Agent Registration cards
 - Workflow DAGs
 - Event schemas
 - Kafka topic schemas
 - Negotiation messages
 - Report and evidence manifests

 /policies
 - Authorization policies
 - IAM models
 - Trust‑zone rules
 
 /tools
 - Detectors
 - Loaders
 - Ingestion systems
 - Publishing tools
 - Risk scoring logic
 - unified_capability_router.py  Platform-wide semantic router.

### **`/tests`**
 Summary:
 Executable tests for platform functionality, workflows, and campaigns.

 Usage:
 Run via pytest or the Makefile to validate platform behavior.

 Contains:
 - Agent registry tests
 - Log‑shipping tests
 - Negotiation flow tests
 - Platform startup/shutdown tests

### **`/campaigns`**
 Summary:
 Human‑facing and agent‑facing communication flows for goal‑oriented campaigns.

 Usage:
 Used by agents and platform components to run structured trust‑building or diagnostic campaigns.

 Contains:
 - Red/Yellow/Green trust‑zone landing pages
 - “Am I a Threat?”
 - “Logs Don’t Lie”
 - Registered Agent onboarding

### **`tree-files.txt`**
 Represents resources that often exist locally but should not be committed to public repositories.
 Helps contributors understand the full structure without exposing sensitive or proprietary materials.
