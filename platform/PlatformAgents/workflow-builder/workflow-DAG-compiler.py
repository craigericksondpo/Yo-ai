# 3. Workflow DAG compiler
# Turn the DSL / spec into a DAG object you can schedule over.

from typing import Set, Tuple
from collections import defaultdict, deque


class WorkflowDAG(BaseModel):
    workflow_id: str
    nodes: Set[str]
    edges: List[Tuple[str, str]]  # (from, to)
    roots: Set[str]
    leaves: Set[str]


def compile_workflow_to_dag(spec: WorkflowSpec) -> WorkflowDAG:
    nodes = {task.id for task in spec.tasks}
    edges = []

    incoming = defaultdict(set)
    outgoing = defaultdict(set)

    # Build edges
    for task in spec.tasks:
        for dep in task.depends_on:
            if dep not in nodes:
                raise ValueError(f"Task {task.id} depends on unknown task {dep}")
            edges.append((dep, task.id))
            outgoing[dep].add(task.id)
            incoming[task.id].add(dep)

    # Compute roots (no incoming) and leaves (no outgoing)
    roots = {n for n in nodes if len(incoming[n]) == 0}
    leaves = {n for n in nodes if len(outgoing[n]) == 0}

    # Detect cycles using Kahn’s algorithm
    in_degree = {n: len(incoming[n]) for n in nodes}
    queue = deque(n for n in nodes if in_degree[n] == 0)
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1
        for neighbor in outgoing[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if visited != len(nodes):
        raise ValueError(f"Workflow {spec.id} contains a cycle")

    return WorkflowDAG(
        workflow_id=spec.id,
        nodes=nodes,
        edges=edges,
        roots=roots,
        leaves=leaves,
    )
# You can store this DAG representation in context storage for the TaskManager to use.
