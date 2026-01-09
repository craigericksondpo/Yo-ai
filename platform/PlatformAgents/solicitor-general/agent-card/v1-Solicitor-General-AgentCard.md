/**
 * This Solicitor-General AgentCard conveys:
 * - Overall details (version, name, description, uses)
 * - Skills: A set of capabilities the agent can perform
 * - Default modalities/content types supported by the agent.
 * - Authentication requirements
 */

/**
* Solicitor-General AgentCard¶
*/
{
  "name": "Solicitor-General",
  "description": "Agent that log all platform events and correlates requests with responses for routing.",
  "url":   "https://privacyportfolio.com/agent-registry/solicitor-general/agent.json",
  "provider": {
    "organization": "PrivacyPortfolio",
    "url": "https://privacyportfolio.com"
  },
  "iconUrl": "https://privacyportfolio.com/agent-registry/solicitor-general/solicitor-general-agent-icon.png",
  "version": "1.0.0",
  "documentationUrl": "https://privacyportfolio.com/agent-registry/solicitor-general/v1-Solicitor-General-AgentCard.md",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": false
  },
  "securitySchemes": {
    "yo-ai": {
      "type": "apiKey",
      "name": "yo-api",
      "in": "header"
    }
  },
  "security": [{ "yo-ai": ["apiKey", "yo-api", "header"] }],
  "defaultInputModes": ["application/json", "text/plain"],
  "defaultOutputModes": ["application/json", "text/plain"],
  "skills": [
    {
      "id": "Log-Event",
      "name": "Log-Event",
      "description": "Inserts a record into the EventLog.",
      "tags": ["audit"],
      "examples": ["Log event"],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": ["application/json", "application/vnd.geo+json", "text/html"]
    },
    {
      "id": "Correlate-Request-Response",
      "name": "Correlate Request-Response",
      "description": "Agent that correlates responses with requests for routing.",
      "tags": ["logEntry", "topic", "request", "response"],
      "examples": [
        "Who responded to request [requestID] on topic [topicID].",
        "Who requested request [responseID] on topic [topicID]."
      ],
      "inputModes": ["application/json"],
      "outputModes": [
        "image/png",
        "image/jpeg",
        "application/json",
        "text/html"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}

 
 /**
 * 6.5.3. DataPart Object¶
 * For conveying structured JSON data. Useful for forms, parameters, or any machine-readable information.
 *  /** Part type - data for DataParts */
 *  kind: "data";
 *  /** Structured data content
 * logEntry
 * 
 *  data: {
 * **/ required  */
 *  [Name: "timestamp"]: string;        /** Precise time of the event in ISO 8601 format */
 *  [Name: "agent_id"]: string;         /** Unique identifier for the agent */
 *  [Name: "agent_name"]: string;       /** Human-readable name of the agent  */
 *  [Name: "provider"]: string;         /** Organization or platform operating the agent */
 *  [Name: "session_id"]: UUID;         /** ID linking events within a single user or task session */
 *  [Name: "user_id"]: DID;             /** Anonymized or hashed user reference (typically a Registered Stakeholder) */
 *  [Name: "event_type"]: string;       /** What happened (e.g., tool_invocation, message_sent, error, handoff, task_completed) */
 *  [Name: "event_id"]: UUID;           /** Unique ID for the event (for deduplication and traceability) */
 *  [Name: "source"]: string;           /** Where the event originated (agent, user, system, external API) */
 *  [Name: "target"]: string;           /** Destination agent or service (for multi-agent routing) */
 *  [Name: "version"]: string;          /** Agent or protocol version at time of event */
 *  [Name: "agent_card_url"]: string;   /** Link to .well-known/agent.json for metadata resolution */
 *  [Name: "tags"]: string;             /** Custom labels for downstream filtering */
 
 * **/ optional agent actions */
 *  [Name: "input"]: string;                  /** Raw input received (e.g., user message, API call) */
 *  [Name: "output"]: string;                 /** Agent’s response or action taken */
 *  [Name: "tool_used"]: string;              /** Name of tool or function invoked (e.g., search_web, generate_image) */ 
 *  [Name: "tool_args"]: string;              /** Parameters passed to the tool */
 *  [Name: "tool_result"]: string;            /** Output returned from the tool */
 *  [Name: "workflow_instance_id"]: string;   /** Ownership or participation in workflow instance */
 
 * **/ optional platform performance */
 *  [Name: "latency_ms"]: string;       /** Time taken to process the event */
 *  [Name: "status"]: string;           /** Success, failure, timeout, etc. */
 *  [Name: "error_message"]: string;    /** Description of failure */
 *  [Name: "retry_count"]: string;      /** Number of retries attempted */
 
 * **/ optional agent compliance */
 *  [Name: "regulatory_flags"]: string;       /** Tags like HIPAA, CPRA, GDPR, WA-MHMD */
 *  [Name: "data_classification"]: string;    /** PII, PHI, sensitive, public */
 *  [Name: "restrictions_status"]: string;    /** Any restrictions related to processing (whether the user opted out of tracking or personalization, contracts, etc.) */
 *  [Name: "evidence_url"]: string;           /** Link to archived evidence (e.g., signed payload, webhook trace) */
 * }
 */

   /** Structured data content
 * generalRequest
 
 *  data: {
 *    [Name: "Request"]: any;
 *    [Type: "Prompt"]: any;
 *    [Value: "Content"]: any;
 *  };
*/ 
 
   /** Structured data content
 * generalResponse

 *   data: {
 *    [Name: "Response"]: any;
 *    [Type: "Output"]: any;
 *    [Value: "Content"]: any;
 *  };
*/

   /** Structured data content
 * generalError

 *  data: {
 *    [Name: "error"]: any;
 *    [Type: "error"]: any;
 *    [Value: "Content"]: any;
 *  };
 */

   /** Part type - optional metadata for DataParts */
 *  metadata: logEntry;
 *  metadata: generalRequest;
 *  metadata: generalResponse;
 *  metadata: generalError;

