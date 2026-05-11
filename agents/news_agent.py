from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from core.state import SubTaskState
from core.prompts import get_prompt, NEWS_ANALYST_FALLBACK
from tools.search import get_search_tool

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def news_analyst_node(state: SubTaskState):
    """Executes the news task for a given ticker."""
    ticker = state["ticker"]
    
    # 1. Fetch prompt from Langfuse
    prompt_template = get_prompt("news_analyst_prompt", NEWS_ANALYST_FALLBACK)
    system_prompt = prompt_template.format(ticker=ticker)
    
    # 2. Use tool to get news
    search_tool = get_search_tool()
    search_results = search_tool.invoke({"query": f"{ticker} stock news recent"})
    
    # 3. Ask LLM to summarize
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Here is the raw search data:\n{search_results}")
    ]
    response = llm.invoke(messages)
    
    # Return the result in a list so the `operator.add` reducer appends it correctly
    return {"completed_tasks": [{
        "task_id": state["task_id"],
        "ticker": ticker,
        "task_type": "news",
        "result": response.content
    }]}
