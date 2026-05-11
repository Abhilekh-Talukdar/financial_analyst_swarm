from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from core.state import GlobalState
from core.prompts import get_prompt, SYNTHESIZER_FALLBACK

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def synthesizer_node(state: GlobalState):
    """Synthesizes all completed sub-tasks into a final report."""
    query = state["query"]
    completed_tasks = state.get("completed_tasks", [])
    
    # Format the reports into a string
    reports_str = ""
    for task in completed_tasks:
        reports_str += f"--- {task['task_type'].upper()} REPORT ({task['ticker']}) ---\n"
        reports_str += f"{task['result']}\n\n"
        
    prompt_template = get_prompt("synthesizer_prompt", SYNTHESIZER_FALLBACK)
    system_prompt = prompt_template.format(query=query, reports=reports_str)
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Please write the final investment memo.")
    ]
    response = llm.invoke(messages)
    
    return {"final_report": response.content}
