# A2A Handler Architecture
## How Agents Talk to Agents

**Platform:** Yo-ai · Native Python · No Third-Party Framework Dependencies  
**A2A Specification:** [https://a2a-protocol.org/latest/specification/](https://a2a-protocol.org/latest/specification/)  
**Status:** Current 

---

## Overview

The Yo-ai platform supports four distinct startup modes for agent interaction. 
Each mode maps to a different entry point, carries different protocol overhead, and is appropriate for different callers. 
All four modes converge on the same SolicitorGeneral routing logic and the same `run(payload, agent_ctx, capability_ctx)` contract — 
the mode affects how a request arrives, not how a capability executes.

`AgentContext.startup_mode` records which mode delivered a request. 
Every Agent Log entry carries this value, making the full request path auditable 
without inspecting transport-level records.

---

## The Four Startup Modes

| Value | Mode | Entry Point | Caller |
|---|---|---|---|
| `"a2a"` | Mode 1 — HTTP A2A | `POST /a2a` via `a2a_transport.py` | Any external caller, third-party agents, curl |
| `"direct"` | Mode 2 — A2A Direct | `SolicitorGeneral.route_a2a()` | Internal platform agents calling each other |
| `"api"` | Mode 3 — API Gateway | `http/openai/api_handler.py` | OpenAI-compatible API clients, AWS API Gateway |
| `"starlette"` | Mode 4 — Starlette/MCP | Starlette-mounted app | MCP clients, streaming consumers |

Every capability `run()` module receives `agent_ctx.startup_mode` and can branch on it for audit purposes 
— but the `(payload, agent_ctx, capability_ctx)` signature never changes regardless of mode.

---

## Architecture Overview

```
External Callers                Platform Agents              Capabilities
─────────────────               ────────────────             ────────────
curl / frontend  ──[Mode 1]──▶  a2a_transport.py
                                       │
OpenAI client    ──[Mode 3]──▶  api_handler.py      ──▶  SolicitorGeneral.route()
                                                               │
MCP client       ──[Mode 4]──▶  starlette app                 │
                                                         ┌─────▼──────────────────┐
Platform agent   ──[Mode 2]──▶  SolicitorGeneral         │  AGENT_REGISTRY        │
                                .route_a2a()             │  local → handle_a2a()  │
                                                         │  lambda → boto3.invoke │
                                                         └────────────────────────┘
                                                               │
                                                    run(payload, agent_ctx, capability_ctx)
```

---

## Core Components

### a2a_transport.py

The transport layer owns the A2A v1.0 JSON-RPC envelope. 
It validates incoming requests, extracts and tracks `correlation_id` and `taskId`, 
delegates to SolicitorGeneral, and wraps responses in compliant envelopes. 
It has no knowledge of capabilities or agents — its only job is protocol correctness.

`taskId` is required in every A2A v1.0 response `metadata` block. 
`a2a_transport.py` always includes it via `_build_response()`. 

Key internal state:
- `self.pending_requests` — `request_id → metadata`, used for correlation tracking
- `self.pending_tasks` — `task_id → task state`, for async task lifecycle

### SolicitorGeneral (solicitor_general.py)

The routing authority. All capability requests pass through SolicitorGeneral regardless of mode. It:

- Builds `AgentContext` (governance layer) and `CapabilityContext` (execution layer) from the inbound envelope
- Strips any caller-supplied `governance_labels` — platform assigns these, callers cannot claim them
- Consults `AGENT_REGISTRY` for Mode 2 dispatch
- Returns a routing decision dict for Mode 1/3/4 handlers to execute

### AgentContext and CapabilityContext

The two-context model separates concerns cleanly. Both are constructed by SolicitorGeneral, not by capability code.

**AgentContext** — governance: who is asking, on whose behalf, under what conditions, and how was it invoked.

| Field | Description |
|---|---|
| `correlation_id` | JSON-RPC request ID. Primary request-response handle. |
| `task_id` | A2A task identifier. Defaults to `correlation_id` if absent. |
| `startup_mode` | Which mode delivered this request: `"a2a"`, `"direct"`, `"api"`, `"starlette"`. |
| `caller` | Identity of the requesting agent or subscriber. |
| `subject_ref` | Lightweight pointer to the subject. Not a data object. |
| `governance_labels` | Platform-assigned only. Never populated from caller input. |

**CapabilityContext** — execution: what this capability needs to run correctly.

| Field | Description |
|---|---|
| `capability_id` | Canonical capability name (e.g. `"Trust.Assign"`). |
| `dry_run` | Execute logic but skip side effects. |
| `trace` | Activate OpenTelemetry tracing (Layer 4, deferred). |
| `input_schema_name` | Derived property: `"trust.assign.input.schema.json"`. Used as Agent Log `event_type` for Entry 1. |
| `output_schema_name` | Derived property: `"trust.assign.output.schema.json"`. Used as Agent Log `event_type` for Entry 2. |

Capability code accesses both contexts as received 
— it never constructs them, and it never imports `AgentContext` or `CapabilityContext` directly. 
Both classes are exposed through `BaseAgent.context_class` and `BaseAgent.capability_context_class` 
for agents that need to construct them (SolicitorGeneral, handlers).

### yo_ai_handler.py

Universal Lambda / HTTP entrypoint for the Yo-ai Platform.

This is the recommended front door for ALL agents on the platform.
Startup Mode 1 (HTTP /a2a POST) and Mode 4 (Starlette/MCP) both land here.

Module-level singletons are constructed once per Lambda execution environment
and reused across warm invocations. Construction order matters:
  1. PlatformEventBus       — in-process pub/sub for PlatformAgents
  2. capability_map          — loaded from shared/artifacts/capability_map.yaml
  3. SolicitorGeneralAgent   — requires event_bus + capability_map
  4. A2AValidator            — independent, no dependencies
  5. A2ATransport            — requires SG + validator + logger

Capability Map:
  The shared capability map at /shared/artifacts/capability_map.yaml is the
  single source of truth for all platform capabilities and routes. It is
  read/write accessible to all agents. Both this handler and api_handler.py
  load from the same file — no capability paths are hard-coded in either.

### http/openai/api_handler.py

Mode 3 entry point. Receives requests from OpenAI-compatible API clients and AWS API Gateway. 
Handles two event shapes: 
- API Gateway HTTP API v2 payload format (with `rawPath` and `body`) and 
- direct Lambda invocation (with `capability` and `payload` fields).

`api_handler.py` is in `http/openai/` because it implements an OpenAI-compatible request surface
— callers that speak OpenAI's API format can reach Yo-ai agents through this handler without speaking A2A directly.

---

## Mode 1 — HTTP A2A (`startup_mode="a2a"`)

Any external caller. The caller knows nothing about internal agent topology 
— it only knows the platform's public HTTP surface. 
All A2A protocol details are handled by `a2a_transport` before any agent code runs.

### Request shape

```json
POST /a2a
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id":      "req_abc123",
  "method":  "a2a/request",
  "params": {
    "targetAgentId": "door-keeper",
    "capability":    "Trust.Assign",
    "payload": {
      "visitorId":   "vis_001",
      "subjectRef":  "user_42"
    },
    "correlationId": "req_abc123",
    "taskId":        "task_001"
  }
}
```

### Request flow

| Step | Layer | Action |
|---|---|---|
| 1 | HTTP Router | Receives `POST /a2a`, parses JSON body, calls `A2ATransport.handle_request(raw)` |
| 2 | A2ATransport | Validates JSON-RPC envelope against A2A v1.0 schema via `A2AValidator` |
| 3 | A2ATransport | Extracts `correlation_id` and `taskId`; records in `pending_requests` |
| 4 | A2ATransport | Calls `sg.route(envelope, request_id, mode="a2a")` |
| 5 | SolicitorGeneral | Builds `AgentContext` (strips caller governance labels) + `CapabilityContext` |
| 6 | Handler | Validates input schema, dispatches to `run(payload, agent_ctx, capability_ctx)` |
| 7 | run() module | Executes capability; returns result dict |
| 8 | Handler | Shapes output, logs completion, builds A2A response envelope |
| 9 | A2ATransport | Wraps in JSON-RPC success envelope with `metadata.taskID`; pops `pending_requests` |
| 10 | HTTP Router | Serialises envelope to JSON, returns HTTP 200 |

### Response shape

```json
{
  "jsonrpc": "2.0",
  "id":      "req_abc123",
  "result": {
    "trustTier":     "registered",
    "trustScore":    0.72
  },
  "metadata": {
    "capability":    "Trust.Assign",
    "taskId":        "task_001",
    "timestamp":     "2026-03-22T14:30:00Z"
  }
}
```

Errors are returned as HTTP 200 with a structured error envelope 
— never as HTTP 4xx/5xx except for truly unhandled exceptions. 
Callers must inspect `result` or `error`, not rely on HTTP status alone.

| Code | HTTP | Meaning |
|---|---|---|
| `INVALID_JSON` | 400 | Malformed request body |
| `MISSING_TARGET_AGENT` | 400 | `params.targetAgentId` absent |
| `UNKNOWN_AGENT` | 200 | `targetAgentId` not in registry |
| `INPUT_VALIDATION_FAILED` | 200 | Capability input schema violation |
| `AI_OUTPUT_VALIDATION_FAILED` | 200 | AI output missing required fields |
| `AGENT_INVOCATION_FAILED` | 500 | Unhandled exception only |

---

## Mode 2 — A2A Direct (`startup_mode="direct"`)

Internal platform agents calling each other. 
Constructs a standard A2A envelope and passes it to `SolicitorGeneral.route_a2a()` 
— which dispatches directly to the target agent's `handle_a2a()` method (local)
or invokes the target's Lambda function (remote). No HTTP round-trip. 
Full A2A protocol semantics preserved.

**The critical property of Mode 2: no other agent code is modified.** 
Calling agents construct the same envelope they always would. 
Called agents receive `(payload, agent_ctx, capability_ctx)` as they always do. 
Only SolicitorGeneral knows the AGENT_REGISTRY exists.

### Calling pattern (from any agent)

```python
# Inside any agent's run() module or capability method
envelope = {
    "jsonrpc": "2.0",
    "id":      agent_ctx.correlation_id,
    "method":  "a2a/request",
    "params": {
        "targetAgentId": "door-keeper",
        "capability":    "Trust.Assign",
        "payload":       { "visitorId": visitor_id },
        "correlationId": agent_ctx.correlation_id,
        "taskId":        agent_ctx.task_id,
    }
}
result = await solicitor_general.route_a2a(envelope)
```

### AGENT_REGISTRY

SolicitorGeneral's registry maps agent names to their dispatch strategy. 
Populated at platform startup — not hardcoded in `solicitor_general.py`.

```python
from agents.solicitor_general.solicitor_general import (
    register_local_agent,
    register_lambda_agent,
)

# Critical-path agents: local in-process, zero network overhead
register_local_agent("door-keeper", DOOR_KEEPER_INSTANCE)

# AI/IO-heavy agents: Lambda, isolated + auto-scaling
register_lambda_agent("data-steward",      "data-steward-handler")
register_lambda_agent("incident-responder", "incident-responder-handler")
```

| Strategy | When to use | Characteristics |
|---|---|---|
| `local` | Critical path, fast decisions, shared state needed | Direct Python method call, zero network, shared process memory |
| `lambda` | AI execution, external I/O, independent scaling | boto3 invocation, isolated resources, stateless |

### Request flow

| Step | Layer | Action |
|---|---|---|
| 1 | Calling agent | Constructs A2A envelope with `targetAgentId`, `capability`, and payload |
| 2 | SolicitorGeneral | `route_a2a()` validates presence of `targetAgentId` and `capability` |
| 3 | SolicitorGeneral | Builds `AgentContext` (`startup_mode="direct"`) + `CapabilityContext` |
| 4 | SolicitorGeneral | Looks up `targetAgentId` in `AGENT_REGISTRY` |
| 5a | SolicitorGeneral (local) | Calls `agent.handle_a2a(capability_id, payload, agent_ctx, capability_ctx)` |
| 5b | SolicitorGeneral (lambda) | `boto3.invoke(FunctionName=function_name, Payload=json.dumps(envelope))` |
| 6 | Target agent | `handle_a2a()` dispatches to the agent's own capability method |
| 7 | run() module | Executes capability; returns result dict |
| 8 | SolicitorGeneral | Wraps result in A2A success envelope |
| 9 | Calling agent | Receives structured response; continues workflow |

### handle_a2a() — the Mode 2 contract

Every `PlatformAgent` subclass that can be a local target overrides `handle_a2a()`. 
The base implementation on `PlatformAgent` raises `NotImplementedError`. 
The pattern is a simple dispatch dict — no new code in any `run()` module:

```python
# In door_keeper.py — the reference pattern for all PlatformAgents
async def handle_a2a(
    self,
    capability_id: str,
    payload: dict,
    agent_ctx,
    capability_ctx,
) -> dict:
    dispatch = {
        "Visitor.Identify":        self.visitor_identify,
        "Trust.Assign":            self.trust_assign,
        "Agent.Authenticate":      self.agent_authenticate,
        # ... all capabilities this agent exposes via Mode 2
    }
    handler = dispatch.get(capability_id)
    if handler is None:
        raise NotImplementedError(
            f"Capability '{capability_id}' not found on DoorKeeperAgent."
        )
    return await handler(payload, agent_ctx, capability_ctx)
```

`NotImplementedError` is caught by `SolicitorGeneral._dispatch_local()` 
and returned as a structured error envelope — it never escapes to the caller.

---

## Mode 3 — API Gateway (`startup_mode="api"`)

OpenAI-compatible API clients and AWS API Gateway. 
The entry point is `http/openai/api_handler.py`. 
This handler speaks the OpenAI API surface 
— callers that know OpenAI's request format can reach Yo-ai capabilities without speaking A2A directly.

`api_handler.py` handles two event shapes from Lambda:

**Shape A — API Gateway HTTP API (v2 payload format):**
```json
{
  "rawPath":        "/agents/door-keeper/TrustAssign",
  "body":           "{...JSON...}",
  "requestContext": { "requestId": "..." }
}
```

**Shape B — Direct Lambda invocation:**
```json
{
  "capability":    "Trust.Assign",
  "payload":       { ... },
  "correlationId": "..."
}
```

### Handler dispatch sequence

```
lambda_handler(event, context)
    │
    ├─ 1. Resolve capability_id
    │      Shape A: rawPath segment → CAPABILITY_ROUTER → capability_id
    │      Shape B: event["capability"]
    │
    ├─ 2. Build AgentContext + CapabilityContext (startup_mode="api")
    │      CapabilityContext built BEFORE schema validation so
    │      capability_ctx.input_schema_name drives both validation
    │      and output shaping from the same source of truth
    │
    ├─ 3. Validate input schema
    │      schema_url = f"https://yo-ai.ai/schemas/{capability_ctx.input_schema_name}"
    │      Dot convention: "trust.assign.input.schema.json"
    │      Matches actual files in training/artifacts/messages/
    │
    ├─ 4. Dispatch to run()
    │      CAPABILITY_DISPATCH[capability_id](payload, agent_ctx, capability_ctx)
    │      NotImplementedError → call_ai() fallback
    │
    ├─ 5. Shape output
    │      output_schema_url = f"https://yo-ai.ai/schemas/{capability_ctx.output_schema_name}"
    │
    └─ 6. Return A2A-compliant envelope with metadata.taskId
```

### CAPABILITY_ROUTER and CAPABILITY_DISPATCH

Both are defined at module level in each handler file. 
`CAPABILITY_ROUTER` maps URL path segments to canonical capability IDs. 
`CAPABILITY_DISPATCH` maps capability IDs to agent methods.

```python
# door_keeper_handler.py
CAPABILITY_ROUTER = {
    "TrustAssign":           "Trust.Assign",
    "AgentAuthenticate":     "Agent.Authenticate",
    "VisitorIdentify":       "Visitor.Identify",
    # ...
}

CAPABILITY_DISPATCH = {
    "Trust.Assign":          AGENT.trust_assign,
    "Agent.Authenticate":    AGENT.agent_authenticate,
    "Visitor.Identify":      AGENT.visitor_identify,
    # ...
}
```

The path segment convention is capability ID with dots removed: 
`Trust.Assign` → `TrustAssign`. 
This is consistent with the route segment derivation in `capability_map_builder.py`.

### Handler singleton pattern

Each Lambda execution environment holds one agent instance, created once at module load:

```python
BUS   = PlatformEventBus()
AGENT = DoorKeeperAgent(slim=True, event_bus=BUS)
LOG   = LogBootstrapper(agent_name=AGENT.name)
```

`slim=True` skips fingerprints, knowledge loading, and tool bootstrap 
— appropriate for a handler that processes one capability per invocation. 
The `event_bus=` parameter is required and enforced by `PlatformAgent.__init__()`.

---

## Mode 4 — Starlette/MCP (`startup_mode="starlette"`)

Starlette-mounted app for MCP clients and streaming consumers. 
Mode 4 uses the same SolicitorGeneral routing path as Modes 1 and 3, 
with `startup_mode="starlette"` set on the `AgentContext`. 
This mode is the correct entry point for:

- MCP (Model Context Protocol) tool servers
- Streaming capability responses
- WebSocket-based agent communication
- Long-running task subscriptions

The Starlette mount point is reserved in `http_router.py` and follows the same capability routing logic. 
Full implementation details are in the Starlette/MCP integration guide.

---

## Mode Comparison

| Dimension | Mode 1 — HTTP A2A | Mode 2 — A2A Direct | Mode 3 — API Gateway | Mode 4 — Starlette |
|---|---|---|---|---|
| `startup_mode` | `"a2a"` | `"direct"` | `"api"` | `"starlette"` |
| Entry point | `POST /a2a` | `sg.route_a2a()` | `api_handler.py` | Starlette app |
| Caller | External / any network | Internal platform agent | API Gateway / OpenAI clients | MCP / streaming clients |
| A2A envelope | Full JSON-RPC v1.0 | Full JSON-RPC v1.0 | OpenAI-compatible shape | Protocol-dependent |
| Schema validation | `a2a_transport` layer | `SolicitorGeneral` | Handler (step 3) | Handler |
| Correlation tracking | `pending_requests` dict | Envelope `id` field | `awsRequestId` | Session/stream ID |
| Network overhead | HTTP + transport | None (in-process or Lambda) | Lambda cold start | WebSocket / stream |
| taskId in response | Required — `metadata.taskID` | In envelope `metadata` | In response envelope | Stream metadata |
| Primary use case | Third-party, frontends, curl | Agent-to-agent calls | AWS API Gateway, OpenAI clients | MCP tooling, streaming |

---

## Platform Agents vs YoAi Agents

| | Platform Agents | YoAi Agents |
|---|---|---|
| Examples | Solicitor-General, Door-Keeper, The-Sentinel, Incident-Responder | Data-Steward, Vendor-Manager, Purchasing-Agent
| Lifecycle | Singleton — one instance per Lambda execution environment | Ephemeral or per-profile |
| Profile | Never — platform agents have no profiles | Yes — represents a person or org |
| Mode 2 | Registered as `local` in AGENT_REGISTRY | Registered as `lambda` in AGENT_REGISTRY |
| `slim=` | `slim=True` in handlers (fast init) | `slim=False` for full governance init |
| `event_bus=` | Required — always injected at construction | Not applicable |
| `showCard()` | Returns basic card only — always | Returns extended card to authenticated callers |
| `handle_a2a()` | Override per agent with dispatch dict | Inherited `NotImplementedError` 
(Lambda entry point handles routing) |

---

## The Logging Contract Across Modes

Every capability invocation — regardless of mode — 
produces exactly two Agent Log entries using `agent_ctx.log()`:

**Entry 1** (capability received, before processing):
```python
agent_ctx.log(
    event_type=capability_ctx.input_schema_name,   # "trust.assign.input.schema.json"
    message="Capability received.",
    data={
        "correlationId": agent_ctx.correlation_id,
        "taskId":        agent_ctx.task_id,
        "startupMode":   agent_ctx.startup_mode,   # records which mode delivered this
        "dryRun":        capability_ctx.dry_run,
    }
)
```

**Entry 2** (capability completed, after processing):
```python
agent_ctx.log(
    event_type=capability_ctx.output_schema_name,  # "trust.assign.output.schema.json"
    message="Capability completed.",
    data={
        "correlationId": agent_ctx.correlation_id,
        "taskId":        agent_ctx.task_id,
        "outcome":       result.get("outcome"),
        "dryRun":        capability_ctx.dry_run,
    }
)
```

`startup_mode` in the log makes the full call path auditable. 
An agent that appears in logs with `startup_mode="direct"` was invoked by another platform agent. 
One with `startup_mode="a2a"` was called from outside the platform.

External tool calls (Vault Adapter, HTTP adapters) produce an additional two entries per the audit bridge pattern 
— one before the call and one after — because external tools do not carry `correlationId` 
and cannot write to Yo-ai logs themselves. See `LOGGING.md` for the complete tool boundary pattern.

---

## capability_map.yaml

The routing table consumed by SolicitorGeneral and all handlers. 
Generated by `capability_map_builder.py` from extended agent cards — never edited by hand. 
Every capability has one entry:

```yaml
capabilities:
  Trust.Assign:
    agent:        door-keeper
    handler:      door-keeper-handler    # derived from handler artifact path="/"
    handlerType:  internal
    inputSchema:  trust.assign.input.schema.json
    outputSchema: trust.assign.output.schema.json
    route:        /agents/door-keeper/TrustAssign
    dryRun:       false
    trace:        false

  Agent.Authenticate:
    agent:        door-keeper
    handler:      authentication-claim-handler.py  # from handler artifact path
    handlerType:  external
    inputSchema:  agent.authenticate.input.schema.json
    outputSchema: agent.authenticate.output.schema.json
    route:        /agents/door-keeper/AgentAuthenticate
    dryRun:       false
    trace:        false

routes:
  /agents/door-keeper/TrustAssign:       Trust.Assign
  /agents/door-keeper/AgentAuthenticate: Agent.Authenticate
```

Adding a new capability requires: 
- a new skill in the agent card, 
- a new `run()` module, 
- and a rebuild of `capability_map.yaml`. 
No routing code changes anywhere.

---

## File Map

```
/
├── http/
│   ├── yo_ai_handler.py            ← HTTP surface (routes only, no logic)
│   └── openai/
│       └── api_handler.py          ← Mode 3: API Gateway / OpenAI-compatible handler
│
├── a2a/
│   ├── a2a_transport.py            ← Mode 1: A2A v1.0 envelope & correlation
│   ├── a2a_validator.py            ← JSON-RPC + A2A schema validation
│   └── schemas/
│       ├── a2a_request.schema.json
│       ├── a2a_response.schema.json
│       └── a2a_error.schema.json
│
├── agents/
│   ├── solicitor_general/
│   │   └── solicitor_general.py    ← Broker: routing, AGENT_REGISTRY, Mode 2 dispatch
│   └── door_keeper/
│       ├── door_keeper.py          ← Agent: capability methods + handle_a2a()
│       ├── door_keeper_handler.py  ← Mode 3 Lambda handler (in http/openai/ mount)
│       └── trust_assign.py         ← run(payload, agent_ctx, capability_ctx)
│
├── core/
│   ├── base_agent.py               ← AgentContext, CapabilityContext, BaseAgent
│   ├── yoai_agent.py               ← YoAiAgent: profile, tools, knowledge, ai_client
│   └── platform_agent.py           ← PlatformAgent + PlatformEventBus
│
├── core/runtime/
│   ├── ai_transform.py             ← call_ai(): knowledge-aware LLM fallback
│   ├── ai_client.py                ← Model resolution: env-first, x-ai block, fallback
│   ├── knowledge_query.py          ← Per-request knowledge retrieval
│   ├── schema_validator.py         ← Input/output schema validation
│   └── logging/
│       ├── log_bootstrapper.py     ← Handler lifecycle logger (LOG.write())
│       ├── sink_loader.py          ← Lazy sink factory (cloudwatch/dynamodb/s3/json)
│       └── [cloudwatch|dynamodb|s3|json_file]_sink.py
│
└── shared/
    ├── artifacts/
    │   └── capability_map.yaml     ← Capability routing table (generated, not edited)
    └── tools/
        ├── bootstrap_tools.py      ← Loads x-artifacts type=tool into ToolRegistry
        ├── tool_registry.py        ← ToolRegistry + ToolResult
        ├── tool_invocation_manager.py  ← Audit-bridge wrapper for tool calls
        └── adapters/
            ├── ap2_client_adapter.py
            ├── http_tool_adapter.py
            └── vault_adapter_tool.py
```

---

## Testing by Mode

### Mode 1 — HTTP A2A

```bash
# Valid request
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", "id": "t1", "method": "a2a/request",
    "params": {
      "targetAgentId": "door-keeper",
      "capability": "Trust.Assign",
      "payload": { "visitorId": "vis_001" }
    }
  }'

# Unknown agent — returns HTTP 200 with UNKNOWN_AGENT error envelope
curl -X POST http://localhost:8000/a2a \
  -d '{"jsonrpc":"2.0","id":"t2","method":"a2a/request","params":{"targetAgentId":"unknown","capability":"Test"}}'

# Missing targetAgentId — returns HTTP 400
curl -X POST http://localhost:8000/a2a \
  -d '{"jsonrpc":"2.0","id":"t3","method":"a2a/request","params":{"capability":"Test"}}'
```

### Mode 2 — A2A Direct

```python
# In-process test — no HTTP server, no Lambda
from agents.solicitor_general.solicitor_general import (
    SolicitorGeneralAgent, register_local_agent, PlatformEventBus
)
from agents.door_keeper.door_keeper import DoorKeeperAgent

bus = PlatformEventBus()
dk  = DoorKeeperAgent(slim=True, event_bus=bus)
sg  = SolicitorGeneralAgent(slim=True, event_bus=bus)
register_local_agent("door-keeper", dk)

result = await sg.route_a2a({
    "jsonrpc": "2.0",
    "id":      "test-001",
    "method":  "a2a/request",
    "params": {
        "targetAgentId": "door-keeper",
        "capability":    "Trust.Assign",
        "payload":       { "visitorId": "vis_001" },
        "correlationId": "test-001",
    }
})
assert "result" in result
```

### Mode 3 — API Gateway

```python
# Simulate API Gateway event directly
from agents.door_keeper.door_keeper_handler import lambda_handler

event = {
    "rawPath": "/agents/door-keeper/TrustAssign",
    "body":    '{"payload": {"visitorId": "vis_001"}, "correlationId": "test-001"}',
    "requestContext": { "requestId": "aws-req-001" }
}

response = lambda_handler(event, context=None)
assert response["statusCode"] == 200

# Or direct invocation shape (Shape B)
event_b = {
    "capability":    "Trust.Assign",
    "payload":       { "visitorId": "vis_001" },
    "correlationId": "test-001"
}
response_b = lambda_handler(event_b, context=None)
assert response_b["statusCode"] == 200
```

### Capability unit test (all modes)

```python
# Test a run() module in complete isolation — no mode, no transport
from agents.door_keeper.trust_assign import run

class MockAgentCtx:
    correlation_id = "unit-001"
    task_id        = "unit-001"
    caller         = None
    startup_mode   = "api"
    def log(self, **kwargs): pass

class MockCapabilityCtx:
    dry_run            = True
    capability_id      = "Trust.Assign"
    input_schema_name  = "trust.assign.input.schema.json"
    output_schema_name = "trust.assign.output.schema.json"

result = await run(
    payload       = { "visitorId": "vis_001" },
    agent_ctx     = MockAgentCtx(),
    capability_ctx= MockCapabilityCtx(),
)
assert result.get("trustTier") is not None
```

---

## Key Principles

**HTTP 500 is reserved for unhandled exceptions only.** 
All validation failures, unknown agents, and capability errors are returned as HTTP 200 with a structured error envelope. 
Callers must inspect `result` or `error`, not rely on HTTP status codes alone.

**No router code changes when adding capabilities.** 
The `UnifiedCapabilityRouter` / SolicitorGeneral routing, `a2a_transport`, and HTTP Router 
are never modified to add a capability. All routing is data-driven via `capability_map.yaml` and `AGENT_REGISTRY`.

**No capability code changes to support Mode 2.** 
`run()` modules are identical across all four modes. 
The mode affects entry point and context assembly only — the capability's logic and signature never change.

**The card is the source of truth.** 
`capability_map.yaml` is generated from extended agent cards, not maintained by hand. 
Handler names, schema names, and routes are all derived from card declarations.

**Logging must never crash an agent.** 
All sink writes are wrapped in `try/except`. 
A failed log write falls through to the stdlib logger (CloudWatch). 
An agent is never interrupted by a logging failure.
