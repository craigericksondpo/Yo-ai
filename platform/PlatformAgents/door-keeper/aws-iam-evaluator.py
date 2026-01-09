# 3. ✔️ AWS IAM Style Policy Engine (JSON Policies + Evaluator)
# aws-iam-evaluator.py is a declarative policy engine that evaluates:
# •	Action (route or operation)
# •	Resource (user_id, task_id, workflow_id)
# •	Principal (authenticated user)
# •	Condition (contextual constraints)

# Usage
# allowed = policy_engine.is_allowed(
#     principal=request.scope["auth"],
#     action="users:GetSelf",
#     resource=f"user:{requested_id}",
#     context={"auth.role": request.scope["auth"].role}
 
# Example Policy Document is in \door-keeper\aws-iam-policy.json

import fnmatch

class PolicyEngine:
    def __init__(self, policies):
        self.policies = policies

    def is_allowed(self, principal, action, resource, context=None):
        context = context or {}

        for stmt in self.policies.get("Statement", []):
            if action not in stmt["Action"]:
                continue

            if not any(fnmatch.fnmatch(resource, r) for r in stmt["Resource"]):
                continue

            # Evaluate conditions
            if "Condition" in stmt:
                for cond, rules in stmt["Condition"].items():
                    if cond == "StringEquals":
                        for key, expected in rules.items():
                            actual = context.get(key)
                            if actual != expected:
                                break
                        else:
                            pass
                        continue
                    return False

            return stmt["Effect"] == "Allow"

        return False
