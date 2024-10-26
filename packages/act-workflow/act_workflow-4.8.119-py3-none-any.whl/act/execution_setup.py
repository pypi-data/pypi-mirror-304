from .execution_manager import ExecutionManager
from .node_context import NodeContext

def chat_handler(context: NodeContext):
    if "error" in context.output_data:
        return context.output_data
    return context.output_data

def slack_handler(context: NodeContext):
    return context.output_data

def chat_to_slack_handler(data: Any):
    if isinstance(data, str) and len(data) > 1000:
        return data[:1000] + "... (truncated)"
    return data

def setup_execution_manager(actfile_path: str) -> ExecutionManager:
    manager = ExecutionManager(actfile_path)
    
    # Register handlers
    manager.workflow_engine.register_node_handler("ChatModels", chat_handler)
    manager.workflow_engine.register_node_handler("Slack", slack_handler)
    manager.workflow_engine.register_edge_handler(
        "chatmodels_test", 
        "slack_test", 
        chat_to_slack_handler
    )
    
    return manager