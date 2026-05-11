from typing import TypedDict, Annotated, List, Dict, Any
import operator

class SubTaskState(TypedDict):
    """Local state for individual worker agents running in parallel."""
    task_id: str
    ticker: str
    task_type: str # 'news' or 'quant'
    result: str

class GlobalState(TypedDict):
    """The main state of the graph."""
    query: str
    tasks: List[Dict[str, Any]] # List of tasks to be spawned
    # The `operator.add` reducer allows parallel agents to append their results safely
    completed_tasks: Annotated[List[SubTaskState], operator.add] 
    final_report: str
