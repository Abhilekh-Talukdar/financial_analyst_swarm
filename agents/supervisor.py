from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from core.state import GlobalState
from core.prompts import get_prompt, SUPERVISOR_FALLBACK
import json
import re

llm = ChatOpenAI(model="gpt-4o", temperature=0) # Using GPT-4o for better JSON adherence

def supervisor_node(state: GlobalState):
    """Takes the query and generates a list of sub-tasks."""
    query = state["query"]
    
    prompt_template = get_prompt("supervisor_prompt", SUPERVISOR_FALLBACK)
    system_prompt = prompt_template.format(query=query)
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content="Generate the task plan in JSON.")
    ]
    response = llm.invoke(messages)
    
    try:
        # Simple extraction in case LLM adds code blocks
        content = response.content
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            content = match.group(0)
            
        tasks = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from supervisor: {e}")
        # Fallback task
        tasks = [{"task_id": "fallback_1", "task_type": "news", "ticker": "AAPL"}]
        
    return {"tasks": tasks, "completed_tasks": []}
