# 4. ✔️ Route Graph Aware Authorization Layer (Perfect for FastA2A)
# You can use this graph:
# •	Nodes = agents/services
# •	Edges = routes (HTTP, WS, internal)
# •	Metadata = ownership, audit events, PII flags, retention
# to enforce:
# •	Which service is allowed to call which service
# •	Which agent can access which route
# •	Which workflows can invoke which downstream components
# •	Which internal edges require special permissions

# Usage
# if not route_graph_authorizer.allowed(
#    caller=request.scope["auth"].service,
#    target_service="TaskManager",
#    route="/tasks",
#    method="POST"
# ):
#    return JSONResponse({"error": "Forbidden"}, status_code=403)
# This provides:
# •	Topology aware authorization
# •	Service to service enforcement
# •	Zero trust internal routing
# •	Audit grade evidence

# Example Route Graph
{
  "nodes": [
    {"id": "SolicitorGeneral", "type": "root-agent"},
    {"id": "TaskManager", "type": "broker"},
    {"id": "Storage", "type": "event-store"}
  ],
  "edges": [
    {
      "from": "SolicitorGeneral",
      "to": "TaskManager",
      "route": "/tasks",
      "method": "POST",
      "authz": ["workflow:submit"]
    },
    {
      "from": "TaskManager",
      "to": "Storage",
      "route": "/tasks/{task_id}/events",
      "method": "POST",
      "authz": ["event:append"]
    }
  ]
}

# Authorization Layer
# route-graph-authorizer.py

class RouteGraphAuthorizer:
    def __init__(self, graph):
        self.graph = graph

    def allowed(self, caller, target_service, route, method):
        for edge in self.graph["edges"]:
            if (
                edge["from"] == caller
                and edge["to"] == target_service
                and edge["route"] == route
                and edge["method"] == method
            ):
                required_perms = edge.get("authz", [])
                return all(p in caller.permissions for p in required_perms)

        return False
