# /agents/README.md

Yo-ai Agent Bundles

## Requirements
- Python 3.13.5

## Yo-ai Platform Agents
Yo-ai uses a "Root agent" called the "Solicitor-General", which serves as the A2A application server.
This "root agent" performs the roles of a FastA2A server without using the FastA2A Framework. 
It brokers all A2A messages, manages all tasks, correlates and routes traffic to agents, 
logs all platform events and publishes these events to Kafka topics for subscribers to consume.
The Solicitor-General is the primary interface for agents and humans to interact with.

The "Door-Keeper" agent logs all inbound traffic and evaluates whether the caller is a registered agent or subscriber
before passing them on to the Solicitor-General for routing.
The Door-Keeper manages identity and access controls for anonymous users in an identity pool,
and identifiable users in a user pool. The Door-Keeper also manages trust tiers for provisioning access to resources. 

The "Workflow-Builder" agent generates workflow plans composed of tasks and messages for orchestration among one or more agents. 
Building workflows dynamically supports autonomous decision-making and execution by agents on the Yo-ai Platform. 

The "Incident-Responder" is a platform agent that catches all unhandled exceptions and can respond to them as 'incidents',
and calls the Workflow-Builder to build remedial workflows it can execute. 

The "Decision-Master" monitors event logs for decision-making events, 
publishes a Decision-Diary topic in Kafka that explains what decisions were made and what the outcomes were.

"The-Advisor", is a reasoning agent that provides guidance, synthesis, and platform expertise to other agents. 
It has full access to shared + agent knowledge, uses a Cognitive-Reasoning-Loop for deeper inference, and tracks whether advice was followed (learning loop).

"The-Custodian", is responsible for platform maintenance, managing the dead-letter-queue subsystem, 
and owns all configuration_change artifacts.

"The-Oracle", performs forecasting, consequence modeling, and machine-learning, and is isolated from shared platform knowledge to avoid bias.

"The-Sentinel", is a listener monitoring event logs for adverse, unusual events, and generates alerts to other PlatformAgents.


## Yo-ai Agents
Another subclass of the BaseAgent class, is the YoAiAgent class. 
These agents are specialists with their own skills, knowledge, tools, and artifacts. 
YoAiAgent are also independent A2A agents that can initiate new capabilities. 
While PlatformAgents often delegate tasks to YoAiAgent, the relationship between the two
is not a Broker-Worker or (Master/Slave) dynamic -- YoAiAgents can refuse to accept tasks and messages.

## Yo-ai 'Special' Agents
The two 'special' YoAiAgents are the Data-Steward, and the Vendor-Manager.
These are special in that they represent real individuals and corporate entities. 
Profiles are used in constructors for injecting this context into each agent.
Multiple instances of the Data-Steward agent can represent different individuals or different profiles of the same individual. 
Multiple instances of Vendor-Manager agents can represent different organizations, or departments and subsidiaries within a single corporate entity.

The Data-Steward and the Vendor-Manager are proxies designed to communicate with each other as authorized representatives of people and organizations. 

## Base Agents
The base class of PlatformAgents and YoAiAgent is defined as 'BaseAgent' in the /core folder.
This class allows 'VisitingAgents' to benefit from common platform services and extends A2A support 
for external agents which lack these capabilities.
