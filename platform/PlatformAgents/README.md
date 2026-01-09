# yo-ai

PlatformAgents README.

## Summary
I use a "Root agent" as a FastA2A application server hosted in my AWS API Gateway. This "root agent" is called the "Solicitor-General" because it receives all requests, sends all responses, and logs all platform events from logfire and CloudWatch which are published into Kafka topics for subscribers.

I also use another platform agent called, the "Door-Keeper", which acts as middleware, intercepting all requests before they are passed on to the Solicitor-General. The Door-Keeper logs all inbound traffic and evaluates whether the caller is a registered agent or subscriber. This determines whether the caller is anonymous within a Cognito identity pool, or identifiable within a user pool, with appropriate access permissions set for each group role.  

There is a "Workflow-Builder" agent which orchestrates tasks and messages among one or more agents, and generates workflow plans and reports.

The only other platform agents which are intentionally not exposed are "The-Sentinel", which generates alerts, the "Incident-Responder", which builds and executes remedial workflows, and the "Decision-Master", which publishes a Decision-Diary topic in Kafka.

These agents are in the "PlatformAgents" folder.
