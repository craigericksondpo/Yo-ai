# Simple Task Template
# This is a simple task template for the solicitor general consisting of a prompt/request, 
# a reply/response, and a task status update message.

# Audit Event	    Meaning	                                TaskState
# -----------       -------                                 ---------
# 1. create task	Task record created, no execution yet	Submitted
# 2. working	    Agent is actively processing	        Working
# 3. completed	    Task finished successfully	            Completed

# 1. Submitted
# The task has been created but not yet executed.
# 1) Sample Prompt
# {
#  "role": "user",
#  "content": "Summarize the following text for me."
# }
# 2) Sample Reply
# (None yet — the agent hasn’t started working.)
# 3) Task Status Update Event
# {
#  "event_type": "task.created",
#  "task_id": "task-123",
#  "timestamp": "2025-12-20T13:00:00Z",
#  "payload": {
#    "status": "submitted"
#  }
# }
#
# Expected context_storage
# •	Empty or minimal stub 
#   o	agent_type
#   o	created_at
#   o	maybe a placeholder for internal message list
# 
# Example context_storage
# {
#   "agent_type": "pydantic-ai",
#   "context": {
#     "internal_messages": [],
#     "execution_trace": []
#   }
# }

# 2. Working
# The agent is actively processing the task.
# 1) Sample Prompt
# {
#  "role": "user",
#  "content": "Summarize the following text for me."
# }
# 2) Sample Reply
# {
#   "role": "assistant",
#   "content": "Working on your summary now..."
# }
# 3) Task Status Update Event
# {
#   "event_type": "task.status.updated",
#   "task_id": "task-123",
#   "timestamp": "2025-12-20T13:00:02Z",
#   "payload": {
#     "status": "working"
#   }
# }
# 
# Expected context_storage
# •	Internal message objects
# (full PydanticAI message format, including tool calls)
# •	Intermediate reasoning
# (scratchpad, chain of thought, planning graphs)
# •	Tool call traces 
# o	raw tool call payloads
# o	tool results
# o	retries
# •	Validation state 
# o	schema validation errors
# o	coercion logs
# •	Execution trace 
# o	timestamps
# o	step numbers
# o	model invocation metadata
# •	Partial outputs 
# o	draft responses
# o	incomplete summaries
# •	Embeddings or vector lookups
# if the agent uses retrieval
# 
# Example context_storage
# {
#   "agent_type": "pydantic-ai",
#   "context": {
#     "internal_messages": [
#       {
#         "role": "user",
#         "content": "Summarize this text...",
#         "raw_tokens": 512
#       },
#       {
#         "role": "model",
#         "intermediate_reasoning": "Plan: extract intro → summarize → validate",
#         "tool_call": {
#           "name": "extract_section",
#           "arguments": { "section": "introduction" }
#         }
#       }
#     ],
#     "execution_trace": [
#       { "step": 1, "action": "parse_input" },
#       { "step": 2, "action": "call_tool:extract_section" }
#     ],
#     "partial_outputs": {
#       "draft_summary": "The introduction discusses..."
#     }
#   }
# }


# 3. Completed
# The task finished successfully.
# 1) Sample Prompt
# (Already provided earlier; no new prompt required.)
# 2) Sample Reply
# {
#   "role": "assistant",
#   "content": "Here is your summary: ..."
# }
# 3) Task Status Update Event
# {
#   "event_type": "task.status.updated",
#   "task_id": "task-123",
#   "timestamp": "2025-12-20T13:00:10Z",
#   "payload": {
#     "status": "completed"
#   }
# }
# 
# Completed
# Task finished successfully.
# Expected context_storage
# •	Final internal messages
# •	Final tool call results
# •	Final reasoning trace
# •	Validation logs
# •	Output generation trace
# •	Cleanup markers
# (some agents prune intermediate state)
# 
# Example context_storage
# {
#   "context": {
#     "internal_messages": [...],
#     "execution_trace": [...],
#     "final_output": "Here is your summary...",
#     "validation": {
#       "schema": "SummaryResponse",
#       "passed": true
#     }
#   }
# }


