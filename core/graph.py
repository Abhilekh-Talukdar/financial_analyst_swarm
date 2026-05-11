from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from core.state import GlobalState, SubTaskState
from agents.supervisor import supervisor_node
from agents.news_agent import news_analyst_node
from agents.quant_agent import quant_analyst_node
from agents.synthesizer import synthesizer_node

def continue_to_tasks(state: GlobalState):
    """
    Map-Reduce routing logic.
    Reads the `tasks` array and uses the `Send` API to dynamically spawn worker nodes.
    """
    tasks = state.get("tasks", [])
    sends = []
    
    for task in tasks:
        task_type = task.get("task_type")
        if task_type == "news":
            sends.append(Send("news_analyst", task))
        elif task_type == "quant":
            sends.append(Send("quant_analyst", task))
            
    return sends

def build_graph():
    builder = StateGraph(GlobalState)
    
    # Add nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("news_analyst", news_analyst_node)
    builder.add_node("quant_analyst", quant_analyst_node)
    builder.add_node("synthesizer", synthesizer_node)
    
    # Add edges
    builder.add_edge(START, "supervisor")
    
    # Map-Reduce conditional edge
    # After supervisor finishes, it fans out to the worker nodes
    builder.add_conditional_edges(
        "supervisor", 
        continue_to_tasks,
        ["news_analyst", "quant_analyst"]
    )
    
    # Fan-in edges: After workers finish, go to synthesizer
    builder.add_edge("news_analyst", "synthesizer")
    builder.add_edge("quant_analyst", "synthesizer")
    builder.add_edge("synthesizer", END)
    
    return builder.compile()
