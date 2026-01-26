📘 README.md Explainer Content
This is the human readable documentation that accompanies the manifest.
# Solicitor-General Capability Manifest

This document describes the capability contract that the Solicitor-General provides to newly arriving agents. It is derived from the platform’s canonical OpenAPI definitions and expresses the task universe in a form suitable for simulation, onboarding, and progressive trust escalation.

## Purpose

The Solicitor-General acts as the universal mediator for all agent-to-agent interactions. Agents do not call each other directly. Instead, they submit task requests to the Solicitor-General, which performs:

- Schema validation  
- Privilege checks  
- Routing to the correct agent  
- Audit envelope generation  
- Correlation of request and response  

This manifest allows a new agent to understand:

1. What tasks exist  
2. What schemas govern those tasks  
3. What privileges are required  
4. How routing and correlation work  
5. How to safely interact with the platform  

## How to Use This Manifest

### 1. Discover Available Tasks
Each task is described with:
- `operationId`  
- `summary`  
- `inputSchemaRef`  
- `outputSchemaRef`  
- `privilegesRequired`  
- `routing` rules  

Agents should not assume they can invoke every task. Privileges are enforced by the Solicitor-General.

### 2. Validate Payloads
All requests must conform to the schemas defined under `schemas`.  
Invalid payloads will be rejected before routing.

### 3. Submit Tasks Through the Solicitor-General
Agents never call other agents directly.  
All interactions flow through the Solicitor-General’s mediation layer.

### 4. Handle Audit Envelopes
Every response includes an `audit` block containing:
- Correlation ID  
- Timestamp  
- Routing metadata  
- Privileges checked  

Agents must preserve this metadata when storing or forwarding results.

### 5. Participate in Progressive Trust Escalation
New agents begin with minimal privileges.  
As they demonstrate correct behavior, the Solicitor-General may grant additional capabilities.

## Why This Manifest Exists

The platform is designed around:

- Loose coupling  
- Schema-driven governance  
- Regulator-grade auditability  
- Cross-agent negotiation  
- Safety and mutual protection  

The capability manifest ensures that every agent—human-built or autonomous—can operate safely within the ecosystem without requiring prior knowledge of other agents’ internal APIs.

## Relationship to OpenAPI

Although this manifest is derived from OpenAPI definitions, it is not an HTTP API surface.  
Instead, it is a **capability contract** that describes the task universe in a way that agents can interpret and act upon.

The Solicitor-General uses the full OpenAPI specification internally to:
- Validate schemas  
- Generate routing metadata  
- Produce audit envelopes  
- Build the Hybrid API Bundle  

Agents receive only the distilled capability manifest.

---

## Summary

This manifest is the onboarding handshake between the platform and a new agent.  
It communicates what the agent can do, how it must behave, and how the Solicitor-General will mediate all interactions.

It is the foundation for safe, accountable, and interoperable agent behavior across the entire ecosystem.
