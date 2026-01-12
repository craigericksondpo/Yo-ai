# Yo-ai: AI Assurance Platform for Consumers and Organizations

Yo-ai is an AI Assurance Platform that enables Consumers and Organizations to establish secure, transparent, and mutually governed A2A (Agent to Agent) communication channels.
Consumers operate a team of AI Agents led by their Data Steward, who manages all personal vendors through a sandboxed proxy agent called the Vendor Manager.
Organizations operate their own team of AI Agents to manage all their consumers through a sandboxed proxy agent — also called the Data Steward — hosted within the organization’s environment.
These proxy agents may connect directly to the actual parties or operate within isolated internal sandboxes.
Both sides rely on Yo-ai’s workflows, policies, and agent bundles to reach shared understanding and explicit consent.

## What Yo-ai Enables
Yo-ai provides a structured way for individuals and organizations to:

-	Open A2A communication channels
-	Negotiate mutually agreed upon data processing agreements
-	Train each other’s AI Agents to “play well with others”
-	Test for impacts to the corresponding party before, during, or after changes in processing
-	Build trust through transparency, primarily by sharing event logs about their agents’ activities

## Who the Yo-ai Platform Serves
Anyone operating one or more AI Agents that interacts with another person, agent, or operator.

## Problems the Yo-ai Platform Solves
-		Distrust. ”Who comes knocking at my door? What are doing? What do you want? How can I engage with you – or not?”
-		High-latency processes. “My agent can produce this now. When can you get back to me?”

## Benefits the Yo-ai Platform Provides
As an evidence-based learning system for autonomous decision-making, Yo-ai provides 'explainability' through log-shipping for a unified system of truth for all participants in a process.  

# **How This Repository Is Structured**

Yo‑ai is a large, modular platform. 
Each top‑level directory has its own purpose and often its own README with deeper detail.


## ** Architecture & Concepts**

### **`/platform`**
The heart of the system.  
Contains the architectural documents, routing templates, storage schemas, platform agents, IAM models, and the A2A server.

Inside you’ll find:

- **Platform Agents** (Decision‑Master, Door‑Keeper, Solicitor‑General, Incident‑Responder, The Sentinel, Workflow‑Builder)  
- **Routing templates** (OpenAPI, AsyncAPI, Graph routes)  
- **Authorization logic** (IAM policies, evaluators, decorators)  
- **Storage schemas** (context, task, evidence)  
- **Design documents** for server components and streaming systems  

If you want to understand how Yo‑ai works under the hood, this is your starting point.


## ** Agent Bundles**

### **`/yo-ai-agents`**
Standalone agent bundles for the consumer‑side and organization‑side teams.

Each agent bundle includes:

- `agent.json` (identity + capabilities)  
- Agent card documentation  
- Training manuals  
- Artifacts (schemas, workflows, IAM policies)  

Training manuals also contain the chat transcripts used to help build each agent.


## ** Workflows & Automation**

### **`/platform/workflows`**  
YAML‑based workflows for negotiation, risk assessment, registration, blocked communication, and more.

### **`/platform/workflow-builder`**  
The DAG compiler, workflow builder logic, and workflow agent bundle.

### **`/artifacts`**  
Workflow DAGs, event schemas, Kafka topic schemas, negotiation messages, and evidence manifests.

If you want to understand how Yo‑ai automates decisions and negotiations, these folders contain the full machinery.


## ** Policies & Assurance**

### **`/platform/policies`**  
Authorization policies, IAM models, and trust‑zone rules.

### **`/yo-ai-agents/*/policies`**  
Agent‑specific authorization and capability policies.

These documents show how Yo‑ai enforces boundaries, trust, and safe interoperability.


## ** Tests & Validation**

### **`/tests`**
Executable tests for:

- Agent cards  
- Agent registry  
- Log shipping  
- Negotiation flows  
- Platform startup/shutdown  


## ** Campaigns & Messaging**

### **`/campaigns`**
Human‑facing and agent‑facing communication flows, including:

- Red/Yellow/Green trust‑zone landing pages  
- “Am I a Threat?”  
- “Logs Don’t Lie”  
- Registered Agent onboarding  

These materials show how Yo‑ai communicates with humans and operators.


## ** Tools & Utilities**

### **`/tools`**
Detectors, ingestion systems, publishing tools, and risk scoring logic.


## ** Private & Non‑Public Artifacts**

### **`tree-files.txt`**
A manifest of files that exist locally but should **not** be committed to public repositories.
This helps contributors understand the full structure without exposing sensitive materials.


