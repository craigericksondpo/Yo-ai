## /core

This folder contains one base class for all agents: Agent,
and two subclasses, PlatformAgent and YoAiAgent.

The purpose of these classes are to enforce this Core Principle:
The agent should never decide whether it is “basic” or “extended.”
The platform decides that by choosing which card to load.

This principle is used across the entire Yo-ai Platform:
-	Door-Keeper decides whether a visitor is authenticated
-	The platform decides whether to expose /auth/ resources
-	The platform decides whether to serve the extended card
-	The agent simply accepts whatever card(s) it is given

This keeps the agent honest and prevents privilege escalation.

Platform Agents differ only by the extended card and environment.
Yo-ai Agents differ only by the extended card.
Visiting Agents differ only by the absence of the extended card.

Below is a clear, accurate diagram of how cards flow through the system and how privilege boundaries are enforced.
                          ┌──────────────────────────────┐
                          │        Solicitor-General      │
                          │  (controls tool base class)   │
                          └───────────────┬──────────────┘
                                          │
                                          │
                         CARD SELECTION DECISION
                                          │
                                          ▼
                 ┌────────────────────────────────────────────┐
                 │                PLATFORM RUNTIME             │
                 │  (decides which cards to give each agent)  │
                 └───────────────────┬────────────────────────┘
                                     │
     ┌───────────────────────────────┼────────────────────────────────────┐
     │                               │                                    │
     ▼                               ▼                                    ▼
┌──────────────┐             ┌────────────────┐                 ┌─────────────────┐
│ VisitingAgent │             │   YoAiAgent    │                 │  PlatformAgent  │
│ (external)    │             │ (internal)     │                 │ (privileged)    │
└──────┬────────┘             └──────┬─────────┘                 └──────┬──────────┘
       │                               │                                │
       │ receives                      │ receives                       │ receives
       │                               │                                │
       ▼                               ▼                                ▼
┌──────────────┐             ┌────────────────┐                 ┌────────────────────┐
│ Public Card   │             │ Public Card    │                 │ Public Card         │
│ (no tools)    │             │ + Extended Card│                 │ + Extended Card     │
└──────────────┘             └────────────────┘                 └────────────────────┘
       │                               │                                │
       ▼                               ▼                                ▼
┌──────────────┐             ┌────────────────┐                 ┌────────────────────┐
│ Limited       │             │ Full Yo-ai     │                 │ Full Platform       │
│ capabilities  │             │ capabilities   │                 │ capabilities        │
└──────────────┘             └────────────────┘                 └────────────────────┘

Key points:
-	Platform runtime decides which cards to load
-	Agent class simply loads whatever it is given
-	Platform agents always receive extended cards
-	Yo-ai agents receive extended cards only when authenticated
-	Visiting agents never receive extended cards
-	Solicitor General controls the tool base class, preventing jailbreaks

## Platform Agents (environment dependent, privileged, internal):
-	decision-master
-	door-keeper
-	incident-responder
-	solicitor-general
-	the-sentinel
-	workflow-builder

These agents:
-	run inside the platform
-	have environmental bindings
-	have privileged tools
-	have access to /auth/ resources
-	always receive the extended card

## Yo-ai Agents 
- complaint-manager
- compliance-validator
- darkweb-checker
- data-anonymizer
- databroker-monitor
- data-steward
- ip-inspector
- profile-builder
- purchasing-agent
- rewards-seeker
- risk-assessor
- socialmedia-checker
- talent-agent
- tech-inspector
- vendor-manager

These agents:
-	run inside the Yo ai agent runtime
-	do not depend on platform environment
-	do not have platform privileges
-	may receive extended cards only when authenticated
-	otherwise run with only the public card

## Visiting Agents
-	external
-	untrusted
-	public card only

