from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from core.state import SubTaskState
from core.prompts import get_prompt, QUANT_ANALYST_FALLBACK
from tools.finance import get_stock_metrics

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def quant_analyst_node(state: SubTaskState):
    """Executes the quant task for a given ticker."""
    ticker = state["ticker"]
    
    # 1. Fetch prompt
    prompt_template = get_prompt("quant_analyst_prompt", QUANT_ANALYST_FALLBACK)
    system_prompt = prompt_template.format(ticker=ticker)
    
    # 2. Use tool to get metrics
    metrics_str = get_stock_metrics.invoke({"ticker": ticker})
    
    # 3. Ask LLM to summarize
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Here are the raw metrics:\n{metrics_str}")
    ]
    response = llm.invoke(messages)
    
    return {"completed_tasks": [{
        "task_id": state["task_id"],
        "ticker": ticker,
        "task_type": "quant",
        "result": response.content
    }]}
