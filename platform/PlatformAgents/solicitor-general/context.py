{
  "internal_messages": [
    {
      "role": "model",
      "raw_prompt_tokens": [...],
      "parsed_tool_call": {...},
      "intermediate_reasoning": "not exposed to A2A"
    }
  ],
  "execution_trace": {...},
  "pydantic_validation_state": {...}
}

# Context-logging and pruning for each snapshot:
# •	snapshot_id
# •	snapshot_type
# •	timestamp
# •	task_id
# •	size (bytes)
# •	reason_created (internal_message, tool_call, retry, validation, partial_output, state_transition, error, auth_required)
# •	pruned (true/false)
# •	pruned_reason (age, state_transition, max_snapshots_exceeded, manual, policy)

