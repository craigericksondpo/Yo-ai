# yo-ai

AI Assurance Platform project README.

## Requirements
- Python 3.14+

## Summary
I use a "Root agent" as a FastA2A application server hosted in my AWS API Gateway. This "root agent" is called the "Solicitor-General" because it receives all requests, sends all responses, and logs all platform events from logfire and CloudWatch which are published into Kafka topics for subscribers.

I also use another platform agent called, the "Door-Keeper", which acts as middleware, intercepting all requests before they are passed on to the Solicitor-General. The Door-Keeper logs all inbound traffic and evaluates whether the caller is a registered agent or subscriber. This determines whether the caller is anonymous within a Cognito identity pool, or identifiable within a user pool, with appropriate access permissions set for each group role.  

There is a "Workflow-Builder" agent which orchestrates tasks and messages among one or more agents, and generates workflow plans and reports.

The only other platform agents which are intentionally not exposed are "The-Sentinel", which generates alerts, the "Incident-Responder", which builds and executes remedial workflows, and the "Decision-Master", which publishes a Decision-Diary topic in Kafka.

These agents are in the "PlatformAgents" folder.

The "A2AServer" folder contains a number of components used to build, maintain, support, and host the Yo-ai Platform. Many of the files in this root directory pertain to FastA2A components, such as broker.py, storage.py, and the A2A Specification.
The "A2AServer" folder includes subfolders: AWS, Kafka, Twilio, Dropbox, data.world, Microsoft, Github, Google, Logfire, NetworkSolutions, Postman, Discord, Slack, crew.ai, and Zoom. 
These subfolders may contain tools, projects, configurations, and documentation, which could be used by Yo-ai and "privileged" Registered Agents as a knowledgebase for building new tools and artifacts.

## Problems solved by this platform architecture
Security: AWS provides a VPC, security group, identity and access controls, monitoring, and lambda functions for each API Gateway endpoint where the FastA2A HTTP Server is hosted.

Transparency: Publishing all requests, tasks, decisions, input and output as events to Kafka in Confluent Cloud, implements the "Storage Class" of the FastA2A application server. Registered agents and subscribers can use these events as history, for adding context, troubleshooting, or to preserve 'explanations' for agent behavior.

Integrity: Every platform event should be traceable to its accountable owner, no matter who invoked it or how many different platforms a workflow touches.

Interoperability: In theory, using the A2A Protocol reduces dependencies on operating systems, programming languages, llm providers, etc. Most Yo-ai agents are A2A-enabled, but are also designed to communicate and interact with agents and callers which do not use the A2A protocol, encouraging them and even boot-strapping A2A agent proxies.

Autonomy: Robust event logging is critical for autonomous agents. Yo-ai agents are 'semi-autonomous', highly-trained under a supervised learning model according to training manuals, custom repositories, and event log analysis. 

