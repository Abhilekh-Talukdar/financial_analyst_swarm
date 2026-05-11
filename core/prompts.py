from langfuse import Langfuse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Langfuse client
langfuse = Langfuse()

def get_prompt(prompt_name: str, fallback: str):
    """
    Tries to fetch the prompt from Langfuse Prompt Management.
    Falls back to a default hardcoded string if not found or if offline.
    """
    try:
        # Assuming you've created these in the Langfuse UI
        prompt = langfuse.get_prompt(prompt_name)
        return prompt.get_langchain_prompt()
    except Exception as e:
        print(f"Could not fetch '{prompt_name}' from Langfuse. Using fallback.")
        from langchain_core.prompts import PromptTemplate
        return PromptTemplate.from_template(fallback)

# -----------------
# Fallback Prompts
# -----------------

SUPERVISOR_FALLBACK = """You are a Lead Financial Analyst. 
The user will ask you to analyze a stock ticker.
Your job is to break this request down into specialized tasks for your sub-agents.
You should ALWAYS assign exactly two tasks:
1. A 'news' task to get recent sentiment.
2. A 'quant' task to get raw financial metrics.

Output a strictly valid JSON array of task objects, where each object has:
- "task_id": a unique string
- "task_type": exactly either "news" or "quant"
- "ticker": the stock ticker symbol

Do NOT wrap the JSON in markdown code blocks. Output raw JSON only.

Example Output:
[
  {{"task_id": "task_1", "task_type": "news", "ticker": "AAPL"}},
  {{"task_id": "task_2", "task_type": "quant", "ticker": "AAPL"}}
]

User Query: {query}
"""

NEWS_ANALYST_FALLBACK = """You are a Market News Sentiment Analyst.
You will receive a stock ticker. Use your web search tool to find recent news.
Summarize the overall market sentiment based on the headlines.

Ticker: {ticker}
"""

QUANT_ANALYST_FALLBACK = """You are a Quantitative Financial Analyst.
You will receive a stock ticker. Fetch the current stock price, P/E ratio, and market cap. 
Write a brief technical summary based on these raw metrics.

Ticker: {ticker}
"""

SYNTHESIZER_FALLBACK = """You are a Lead Financial Analyst.
You assigned sub-tasks to your team, and they have returned their reports.
Write a cohesive, professional investment memo in Markdown format that synthesizes their findings.
Make sure to include a clear conclusion.

Original Query: {query}

Sub-agent Reports:
{reports}
"""
