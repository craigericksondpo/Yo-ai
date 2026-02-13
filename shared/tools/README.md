# yo-ai-assurance-platform \ shared-tools

The "shared-tools" folder contains general purpose tools used by multiple Yo-ai agents and "privileged" Registered Agents on the Yo-ai Platform.
For example, the "capabilityLoader" initializes extended capabilities for an agent's skills, based on its authenticatedextendedcard.

Some tools, authored by organizations and individuals outside of PrivacyPortfolio and Craig Erickson on the Yo-ai Platform, have been properly attributed and are pulled from the original public repositories when no modifications are needed. Many of these tools are used in conformity tests (A2A, FastA2A, Starlette, the Google Agent Development Kit, and other frameworks).

Examples of tools authored by PrivacyPortfolio for the Yo-ai Platform include:
"dataworld-publishing", which publishes evidence artifacts and datasets in a public data catalog. One requirement for using this tool is membership in the PrivacyPortfolio organization on data.world. It does not restrict anyone from viewing, querying, or downloading artifacts from the catalog.

"multi-channel-evidence-ingestion-system" is a tool for sourcing artifacts and datasets from multiple transport channels: email, phone, SMS texts, API, file, video, chats, sockets, etc. which replaces ActivityLogs manually populated in Excel.

"Blocked-Communication-Detector" is a Python script that detects actions taken to prevent messages from being delivered to intended recipients or designated process endpoints, or detects evasive actions to intentionally or accidently hide internal responses such as "email marked as spam", "email read", or "service unavailable".

"Chatbot-Buster" is a tool that analyzes chatbot widgets, frames, and scripts to identify owner/operators, data collected, tracking technologies, and security and privacy controls.

"Risk-Scoring" is a tool that calculates a risk score based on my personal preferences, but can be modified to implement any other criteria or scoring algorithm.
For example, the Data-Steward agent has a more stringent risk-scoring system than any other public-facing agent, because it is used to determine access to PII with varying degrees of sensitivity. The Data-Steward's scoring system is in the "Yo-ai_Platform\Yo-ai-Agents\Data-Steward\Tools" folder.

