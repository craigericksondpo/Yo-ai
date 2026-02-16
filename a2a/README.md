# FastA2A Routing Model (Contributor Guide)

This document explains how routing works across the platform and where
contributors should add new capabilities, handlers, and constructors.

---

## 1. Two Routers, Two Responsibilities

### A. HTTP Router (`/http/routes/http_router.py`)
This is the only HTTP surface exposed by the Solicitor-General.

It defines:
- Landing page (`/`)
- Public agent card (`/.well-known/agent-card.json`)
- Identity endpoints (`/register`, `/auth`, `/permissions`)
- Extended agent card (`/agent/extended`)
- A2A entrypoint (`/a2a`)
- Optional mounts (`/api`, `/internal`, `/docs`)

It does **not** contain semantic logic.

---

### B. Unified Capability Router (`/shared/tools/unified_capability_router.py`)
This is the platform-wide semantic authority.

It:
- Interprets A2A envelopes
- Dispatches by messageType
- Dispatches by capability
- Hydrates agents via constructors
- Produces auditable responses

All contributors should register:
- New capabilities
- New messageTypes
- New agent constructors

in this router or in `capability_map.yaml`.

---

## 2. Capability Registration

Capabilities are declared in:
/shared/tools/capability_map.yaml


Each capability maps to a Python handler.

---

## 3. MessageType Dispatch

MessageTypes override capabilities and are dispatched first.

Example:
messageType: Profile.Patch


---

## 4. Agent Constructors

Agent constructors hydrate agents with profile metadata.

Declared in:
constructors: DataSteward: data_steward_constructor



---

## 5. A2A Flow

1. HTTP request hits `/a2a`
2. HTTP router forwards envelope to Unified Capability Router
3. Semantic router:
   - checks messageType
   - checks capability
   - hydrates agent
   - invokes handler
4. Response returned as A2A envelope

---

## 6. Adding New Capabilities

1. Add entry to `capability_map.yaml`
2. Register handler in `unified_capability_router.py`
3. Implement handler in your agent

---

This routing model ensures:
- Clear separation of HTTP vs semantics
- Contributor visibility
- Schema-driven capability exposure
- Extensible, future-proof routing
