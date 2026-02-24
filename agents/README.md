# /agents/README.md

Yo-ai Agent Bundles

## Requirements
- Python 3.13.5

## Yo-ai Platform Agents
Yo-ai uses a "Root agent" as a FastA2A application server hosted in AWS API Gateway. 
This "root agent" is called the "Solicitor-General": 
acting as a FastA2A Broker, it receives all requests, sends all responses, logs all platform events and publishes the events to Kafka topics for subscribers to consume.
The Solicitor-General is the primary interface for agents and humans to interact with.
FastA2A Storage and Task roles are also managed by the Solicitor-General, which dispatches messages to other Yo-ai-agents and maintains the state of long-running tasks and workflows.

Another platform agent, the "Door-Keeper", acts as middleware, intercepting all requests before they are passed on to the Solicitor-General. The Door-Keeper logs all inbound traffic and evaluates whether the caller is a registered agent or subscriber. This determines whether the caller is anonymous within a Cognito identity pool, or identifiable within a user pool, with appropriate access permissions set for each group role. The Door-Keeper is responsible for authentication, identity, and assigns trust tiers for provisioning access to resources. 

The "Workflow-Builder" agent generates workflow plans used by the Solicitor-General to orchestrate tasks and messages among one or more agents. Building workflows dynamically by agents and for agents, supports autonomous decision-making and execution on the Yo-ai Platform. 

The "Incident-Responder" is a platform agent that catches all unhandled exceptions and can respond to them as 'incidents' by asking the Workflow-Builder to build remedial workflows it can execute. 

The "Decision-Master", which monitors event logs for decision-making events, publishes a Decision-Diary topic in Kafka that explains what decisions were made and what the outcomes were.

"The-Advisor", is a reasoning agent that provides guidance, synthesis, and platform expertise to other agents. It has full access to shared + agent knowledge, uses a Cognitive-Reasoning-Loop for deeper inference, and tracks whether advice was followed (learning loop).

"The-Custodian", is a privileged PlatformAgent responsible for platform maintenance, managing the dead-letter-queue subsystem, and owns all configuration_change artifacts.

"The-Oracle", which performs forecasting, consequence modeling, and learning, is isolated from shared platform knowledge to avoid bias.

"The-Sentinel", which monitors event logs for adverse, unusual events, generates alerts and rounds out this class of PlatformAgents, which is defined in the /core folder.


## Yo-ai Agents
Another subclass of the Agent class, is the Yo-ai-agent class. These agents are specialists with their own skills, knowledge, tools, and artifacts; and they are also independent A2A agents that can initiate new capabilities. PlatformAgents often delegate tasks to Yo-ai-agents, but the relationship between the two is not a Broker-Worker or (Master/Slave) dynamic -- Yo-ai-agents can refuse to accept tasks and messages.

## Yo-ai 'Special' Agents
The two 'special' Yo-ai-agents are the Data-Steward, and the Vendor-Manager.
These are special in that they represent real individuals and corporate entities. 
Profiles are used in constructors for injecting this context into each agent.
Multiple instances of the Data-Steward agent could represent different profiles of the same individual, just as a corporate entity might be represented by a number of Vendor-Manager agents injected with OrgProfiles from various subsidiaries.
The Data-Steward and the Vendor-Manager are designed to communicate with each other as authorized representatives of people and organizations, and are considered as "leaders of their teams". 

## Base Agents
The base class of PlatformAgents and Yo-ai-agents is defined as 'Agent' in the /core folder.
This class includes 'VisitingAgents' and 'RegisteredAgents' to support A2A interactions across domain boundaries.
