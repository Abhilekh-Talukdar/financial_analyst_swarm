# Financial Analyst Swarm 📈🤖

An advanced, multi-agent financial research system built with **LangGraph** (for dynamic orchestration) and **Langfuse** (for deep observability and tracing).

## Overview
This project demonstrates the **Map-Reduce (Swarm)** pattern in AI agent architecture. 

A Lead Analyst (Supervisor) receives a user query (e.g., "Analyze Apple's current market position"), dynamically spawns specialized sub-agents (News Analyst, Quant Analyst) to run in parallel using LangGraph's `Send` API, and then synthesizes their findings into a final markdown investment memo.

## Features
- **Dynamic Parallel Execution:** Agents run concurrently to save time and reduce latency.
- **Deep Observability:** Fully integrated with Langfuse to trace concurrent executions, manage prompts externally, and track token costs per sub-agent.
- **Real-time Data:** Uses Tavily for live web search and `yfinance` for live stock metrics.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abhilekh-Talukdar/financial_analyst_swarm.git
   cd financial_analyst_swarm
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install langgraph langchain-openai langfuse tavily-python python-dotenv yfinance langchain-community
   ```

4. **Configure Environment Variables:**
   Rename `.env.example` to `.env` (or create a `.env` file) and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
   LANGFUSE_SECRET_KEY=your_langfuse_secret_key
   LANGFUSE_HOST=https://cloud.langfuse.com
   TAVILY_API_KEY=your_tavily_key
   ```

5. **Run the Swarm:**
   ```bash
   python main.py
   ```
   *Watch the terminal for progress, and check your Langfuse dashboard to view the trace waterfall!*
