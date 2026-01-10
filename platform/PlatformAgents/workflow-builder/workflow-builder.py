from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field
from datetime import timedelta


class RetryPolicy(BaseModel):
    max_attempts: int = 3
    backoff_strategy: Literal["fixed", "exponential"] = "exponential"
    initial_delay_seconds: int = 5
    max_delay_seconds: int = 300


class TimeoutPolicy(BaseModel):
    soft_timeout_seconds: Optional[int] = None  # warn / heartbeat
    hard_timeout_seconds: Optional[int] = None  # fail task


class TaskSpec(BaseModel):
    id: str
    type: str  # logical type, maps to a worker capability
    name: Optional[str] = None
    description: Optional[str] = None

    # DAG dependencies
    depends_on: List[str] = Field(default_factory=list)

    # Input can be raw data or a template that resolves from previous results
    input_template: Dict = Field(default_factory=dict)

    # Policies
    retry_policy: Optional[RetryPolicy] = None
    timeout_policy: Optional[TimeoutPolicy] = None

    # Arbitrary metadata for routing, tags, etc.
    tags: Dict[str, str] = Field(default_factory=dict)


class WorkflowMetadata(BaseModel):
    owner: Optional[str] = None
    created_by_agent: Optional[str] = None
    labels: Dict[str, str] = Field(default_factory=dict)


class WorkflowSpec(BaseModel):
    id: str
    name: Optional[str] = None
    description: Optional[str] = None

    tasks: List[TaskSpec]
    metadata: WorkflowMetadata = WorkflowMetadata()

    # Global defaults
    default_retry_policy: RetryPolicy = RetryPolicy()
    default_timeout_policy: TimeoutPolicy = TimeoutPolicy()

    def get_task(self, task_id: str) -> TaskSpec:
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise KeyError(f"Task {task_id} not found in workflow {self.id}")
