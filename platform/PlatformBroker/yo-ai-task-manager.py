# 8. TaskManager agent class
# This is your broker / scheduler. It:
# • Loads the workflow spec and DAG
# • Maintains runtime state per task (status, retries, timestamps)
# • Periodically scans for runnable tasks
# • Dispatches them to Worker agents
# • Handles retries/timeout
# • Emits Kafka + Logfire events
# 
# Supporting runtime models

from enum import Enum

class TaskRuntimeStatus(str, Enum):
    PENDING = "pending"        # created, not yet scheduled
    SCHEDULED = "scheduled"    # scheduled for dispatch
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"

class TaskRuntimeState(BaseModel):
    task_id: str
    status: TaskRuntimeStatus = TaskRuntimeStatus.PENDING
    worker_id: Optional[str] = None
    retry_state: RetryState = RetryState()
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_heartbeat_at: Optional[datetime] = None
    last_error: Optional[str] = None

class WorkflowRuntimeState(BaseModel):
    workflow_id: str
    tasks: Dict[str, TaskRuntimeState]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: Literal["created", "running", "completed", "failed", "cancelled"] = "created"

# TaskManager implementation (sync loop version)
import time
from typing import Callable

class TaskManager:
    def __init__(
        self,
        workflow_id: str,
        store: WorkflowStore,
        a2a_client,  # your FastA2A client for sending tasks
        poll_interval_seconds: int = 5,
        resolve_input_fn: Optional[Callable[[WorkflowSpec, TaskSpec, WorkflowRuntimeState], Dict]] = None,
        worker_selector_fn: Optional[Callable[[TaskSpec], str]] = None,
    ):
        self.workflow_id = workflow_id
        self.store = store
        self.a2a_client = a2a_client
        self.poll_interval_seconds = poll_interval_seconds
        self.resolve_input_fn = resolve_input_fn or self.default_resolve_input
        self.worker_selector_fn = worker_selector_fn or self.default_worker_selector

        self.spec: WorkflowSpec = self.store.get_workflow_spec(workflow_id)
        self.dag: WorkflowDAG = compile_workflow_to_dag(self.spec)
        self.runtime_state = WorkflowRuntimeState(
            workflow_id=workflow_id,
            tasks={
                t.id: TaskRuntimeState(task_id=t.id)
                for t in self.spec.tasks
            },
            created_at=datetime.utcnow(),
        )

    def default_resolve_input(
        self,
        spec: WorkflowSpec,
        task_spec: TaskSpec,
        runtime: WorkflowRuntimeState,
    ) -> Dict:
        # For now, just pass the template as-is.
        # You can later add Jinja2/template resolution from prior task results.
        return task_spec.input_template

    def default_worker_selector(self, task_spec: TaskSpec) -> str:
        # Simple: route by tag or type.
        group = task_spec.tags.get("worker_group", task_spec.type)
        return f"worker::{group}"

    def start(self):
        log_workflow_event("workflow.started", self.workflow_id)
        self.runtime_state.status = "running"
        self.runtime_state.started_at = datetime.utcnow()

        while True:
            if self._is_workflow_finished():
                break
            self._scheduler_iteration()
            time.sleep(self.poll_interval_seconds)

        # Final event
        final_status = self.runtime_state.status
        log_workflow_event(
            f"workflow.{final_status}",
            self.workflow_id,
            metadata={
                "completed_at": self.runtime_state.completed_at.isoformat()
                if self.runtime_state.completed_at else None
            },
        )

    def _is_workflow_finished(self) -> bool:
        tasks = self.runtime_state.tasks.values()
        if all(t.status == TaskRuntimeStatus.COMPLETED for t in tasks):
            self.runtime_state.status = "completed"
            self.runtime_state.completed_at = datetime.utcnow()
            return True

        if any(t.status == TaskRuntimeStatus.FAILED for t in tasks):
            # You can choose to allow partial failure; here we fail the workflow.
            self.runtime_state.status = "failed"
            self.runtime_state.completed_at = datetime.utcnow()
            return True

        return False

    def _scheduler_iteration(self):
        now = datetime.utcnow()

        for task_spec in self.spec.tasks:
            rt = self.runtime_state.tasks[task_spec.id]

            if rt.status in {
                TaskRuntimeStatus.COMPLETED,
                TaskRuntimeStatus.RUNNING,
                TaskRuntimeStatus.CANCELLED,
            }:
                continue

            # Check dependencies
            if not self._dependencies_satisfied(task_spec):
                continue

            # Handle failed or timed-out tasks: retry if allowed
            if rt.status in {TaskRuntimeStatus.FAILED, TaskRuntimeStatus.TIMED_OUT}:
                effective_retry_policy = task_spec.retry_policy or self.spec.default_retry_policy
                if should_retry(effective_retry_policy, rt.retry_state, now):
                    self._dispatch_task(task_spec, rt, now)
                else:
                    # no more retries, treat as failed
                    rt.status = TaskRuntimeStatus.FAILED
                continue

            # Pending: dispatch it
            if rt.status in {TaskRuntimeStatus.PENDING, TaskRuntimeStatus.SCHEDULED}:
                self._dispatch_task(task_spec, rt, now)

            # Timeout checks for running tasks
            if rt.status == TaskRuntimeStatus.RUNNING and rt.started_at:
                effective_timeout_policy = task_spec.timeout_policy or self.spec.default_timeout_policy
                if is_hard_timeout(effective_timeout_policy, rt.started_at, now):
                    rt.status = TaskRuntimeStatus.TIMED_OUT
                    rt.last_error = "Hard timeout exceeded"
                    log_task_event(
                        "task.timed_out",
                        self.workflow_id,
                        task_spec.id,
                        task_spec.type,
                        worker_id=rt.worker_id,
                        attempt=rt.retry_state.attempts,
                        status=rt.status,
                        details={"reason": "hard_timeout"},
                    )

    def _dependencies_satisfied(self, task_spec: TaskSpec) -> bool:
        for dep in task_spec.depends_on:
            dep_state = self.runtime_state.tasks[dep]
            if dep_state.status != TaskRuntimeStatus.COMPLETED:
                return False
        return True

    def _dispatch_task(self, task_spec: TaskSpec, rt: TaskRuntimeState, now: datetime):
        # Register retry attempt
        effective_retry_policy = task_spec.retry_policy or self.spec.default_retry_policy
        rt.retry_state = register_attempt(effective_retry_policy, rt.retry_state, now)

        # Determine worker
        worker_id = self.worker_selector_fn(task_spec)
        rt.worker_id = worker_id
        rt.status = TaskRuntimeStatus.RUNNING
        rt.started_at = now

        log_task_event(
            "task.dispatched",
            self.workflow_id,
            task_spec.id,
            task_spec.type,
            worker_id=worker_id,
            attempt=rt.retry_state.attempts,
            status=rt.status,
            details={"input_template": task_spec.input_template},
        )

        # Send to worker via FastA2A
        task_input = self.resolve_input_fn(self.spec, task_spec, self.runtime_state)
        # pseudo-code: adjust to your actual A2A client
        self.a2a_client.send_task(
            agent_id=worker_id,
            task_id=task_spec.id,
            workflow_id=self.workflow_id,
            input=task_input,
        )

    # This method is called by worker result handler
    def handle_task_result(
        self,
        task_id: str,
        status: Literal["completed", "failed"],
        worker_id: str,
        error: Optional[str] = None,
    ):
        rt = self.runtime_state.tasks[task_id]
        rt.worker_id = worker_id
        now = datetime.utcnow()
        if status == "completed":
            rt.status = TaskRuntimeStatus.COMPLETED
            rt.completed_at = now
            log_task_event(
                "task.completed",
                self.workflow_id,
                task_id,
                self.spec.get_task(task_id).type,
                worker_id=worker_id,
                attempt=rt.retry_state.attempts,
                status=rt.status,
            )
        else:
            rt.status = TaskRuntimeStatus.FAILED
            rt.last_error = error or "Unknown error"
            log_task_event(
                "task.failed",
                self.workflow_id,
                task_id,
                self.spec.get_task(task_id).type,
                worker_id=worker_id,
                attempt=rt.retry_state.attempts,
                status=rt.status,
                details={"error": error},
            )

# You’d wire handle_task_result to the A2A callback or the topic where workers publish their results.

# 4. Retry/timeout policy module
# A small standalone module the TaskManager uses for scheduling decisions.

from datetime import datetime, timedelta
from typing import Optional

class RetryState(BaseModel):
    attempts: int = 0
    last_attempt_at: Optional[datetime] = None
    next_attempt_at: Optional[datetime] = None

def compute_next_backoff(
    retry_policy: RetryPolicy, attempt: int
) -> int:
    if attempt <= 0:
        return retry_policy.initial_delay_seconds

    if retry_policy.backoff_strategy == "fixed":
        delay = retry_policy.initial_delay_seconds
    else:  # exponential
        delay = retry_policy.initial_delay_seconds * (2 ** (attempt - 1))

    return min(delay, retry_policy.max_delay_seconds)

def should_retry(
    retry_policy: RetryPolicy,
    retry_state: RetryState,
    now: datetime,
) -> bool:
    if retry_state.attempts >= retry_policy.max_attempts:
        return False
    if retry_state.next_attempt_at is None:
        return True
    return now >= retry_state.next_attempt_at

def register_attempt(
    retry_policy: RetryPolicy,
    retry_state: RetryState,
    now: datetime,
) -> RetryState:
    new_attempt = retry_state.attempts + 1
    delay_sec = compute_next_backoff(retry_policy, new_attempt - 1)
    return RetryState(
        attempts=new_attempt,
        last_attempt_at=now,
        next_attempt_at=now + timedelta(seconds=delay_sec),
    )

def is_soft_timeout(
    timeout_policy: TimeoutPolicy,
    started_at: datetime,
    now: datetime,
) -> bool:
    if not timeout_policy.soft_timeout_seconds:
        return False
    return (now - started_at).total_seconds() > timeout_policy.soft_timeout_seconds

def is_hard_timeout(
    timeout_policy: TimeoutPolicy,
    started_at: datetime,
    now: datetime,
) -> bool:
    if not timeout_policy.hard_timeout_seconds:
        return False
    return (now - started_at).total_seconds() > timeout_policy.hard_timeout_seconds


