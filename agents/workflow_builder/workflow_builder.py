# workflow_builder.py

import json
from core.platform_agent import PlatformAgent

class WorkflowBuilderAgent(PlatformAgent):
    """
    The Workflow Builder is a platform agent responsible for:
    - building complex workflows
    """
    def __init__(self):
        super().__init__()
