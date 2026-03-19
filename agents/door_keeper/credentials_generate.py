# agents/door_keeper/credentials_generate.py

async def run(payload, agent_ctx, capability_ctx):
    """
    Capability: Credentials.Generate
    Generates credentials for RegisteredAgents and RegisteredSubscribers.

    This capability is the long-term replacement for the API Keys stopgap
    (see API_KEYS.docx). Once operational, agents receive Door-Keeper-issued
    credentials instead of manually provisioned API keys.

    Credential types:
      - api-key      : Temporary bridge credential (current stopgap)
      - mtls-cert    : Client certificate signed by platform CA
                       (see ClientCertificates.docx — issue_client_cert() pattern)
      - capability-token : Scoped token for specific capability access

    Subject types:
      - RegisteredAgent
      - RegisteredSubscriber

    Args:
        payload        (dict): Pre-extracted capability input.
        agent_ctx      (AgentContext): Governance context.
        capability_ctx (CapabilityContext): Execution context — dry_run, trace.
    """

    subject_id      = payload.get("subjectId")
    subject_type    = payload.get("subjectType")     # "RegisteredAgent" | "RegisteredSubscriber"
    credential_type = payload.get("credentialType")  # "api-key" | "mtls-cert" | "capability-token"
    scope           = payload.get("scope", [])       # Capability scopes for capability-token

    # Stub: returns placeholder credential.
    # Real implementation:
    #   api-key      → generate + store in FastA2A Storage, attach to usage plan
    #   mtls-cert    → invoke issue_client_cert() against platform CA
    #   capability-token → issue scoped JWT signed by platform
    stub_credential = {
        "api-key":           {"apiKey": "stub-key-xyz"},
        "mtls-cert":         {"certPath": "stub-cert-path", "keyPath": "stub-key-path"},
        "capability-token":  {"token": "stub-token-abc", "scope": scope},
    }.get(credential_type, {"raw": "stub-credential"})

    result = {
        "subjectId":       subject_id,
        "subjectType":     subject_type,
        "credentialType":  credential_type,
        "credential":      stub_credential,
        "scope":           scope,
        "correlationId":   agent_ctx.correlation_id,
        "taskId":          agent_ctx.task_id,
        "dryRun":          capability_ctx.dry_run,
        "status":          "stub",
    }

    agent_ctx.log(
        event_type="Credentials.Generate",
        message="Credential generation attempted.",
        data={
            "subjectId":      subject_id,
            "subjectType":    subject_type,
            "credentialType": credential_type,
            "scope":          scope,
            # credential value intentionally excluded — never log issued credentials
            "dryRun":         capability_ctx.dry_run,
            "correlationId":  agent_ctx.correlation_id,
            "taskId":         agent_ctx.task_id,
        }
    )

    return result
