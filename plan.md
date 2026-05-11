# Financial Analyst Swarm - Project Plan

This document outlines the phase-wise implementation plan for building a multi-agent financial research swarm using LangGraph (for dynamic Map-Reduce orchestration) and Langfuse (for tracing and observability).

## Phase 1: Environment & Infrastructure Setup
**Goal:** Prepare the workspace, install dependencies, and connect to APIs.
- [ ] Initialize a new Python virtual environment.
- [ ] Install required libraries: `langgraph`, `langchain-openai`, `langfuse`, `tavily-python` (for search), `python-dotenv`, `yfinance` (optional, for real stock data).
- [ ] Create a `.env` file and configure API Keys:
  - `OPENAI_API_KEY`
  - `LANGFUSE_SECRET_KEY`
  - `LANGFUSE_PUBLIC_KEY`
  - `LANGFUSE_HOST`
  - `TAVILY_API_KEY` (or other search API)
- [ ] Set up the basic directory structure (e.g., `agents/`, `tools/`, `core/`).

## Phase 2: State Definition & Prompt Management (Langfuse)
**Goal:** Define the data structures that flow through the graph and set up externalized prompts.
- [ ] Define the **Global State** (TypedDict or Pydantic) containing the original query, the list of sub-tasks, and the final synthesized report.
- [ ] Define the **Sub-Task State** for the individual agents running in parallel.
- [ ] **Langfuse Action:** Create prompt templates in the Langfuse UI for the different personas:
  - `supervisor_prompt`: Instructs the agent to break down a query into specialized tasks.
  - `news_analyst_prompt`: Instructs the agent to summarize market sentiment.
  - `quant_analyst_prompt`: Instructs the agent to evaluate raw financial metrics.
  - `synthesizer_prompt`: Instructs the agent to write a cohesive markdown report from raw notes.
- [ ] Write Python utility functions to fetch these prompts dynamically from Langfuse.

## Phase 3: Building the Sub-Agents & Tools
**Goal:** Create the worker nodes that perform the actual research.
- [ ] **News Analyst Node:** Create an agent that uses a web search tool to find recent articles about a given ticker and summarizes the sentiment.
- [ ] **Quant Analyst Node:** Create an agent that uses `yfinance` or a mock tool to fetch current price, P/E ratio, and market cap, then provides a brief technical summary.
- [ ] *(Optional)* **SEC Filings Node:** Implement a basic RAG pipeline over recent 10-K filings using LangChain.

## Phase 4: Graph Orchestration (LangGraph Map-Reduce)
**Goal:** Tie everything together using LangGraph's `Send` API for parallel execution.
- [ ] **Supervisor Node:** Implement the logic that takes the user query, calls the LLM, and returns a list of tasks (e.g., "Assign News Analyst to AAPL", "Assign Quant Analyst to AAPL").
- [ ] **Map-Reduce Logic:** Write the conditional routing function that maps the generated tasks to their respective nodes using LangGraph's `Send` API (dynamic fan-out).
- [ ] **Synthesizer Node:** Implement the node that gathers the outputs from all parallel agents and writes the final investment memo (fan-in).
- [ ] Compile the graph (`StateGraph`).

## Phase 5: Observability, Tracing & Evaluation (Langfuse)
**Goal:** Execute the graph and monitor its behavior deeply.
- [ ] Wrap the graph execution with the `LangchainCallbackHandler` from Langfuse.
- [ ] Run test queries (e.g., "Analyze TSLA's current market position").
- [ ] **Langfuse Action:** Inspect the trace waterfall in the Langfuse UI. Verify that the sub-agents executed concurrently.
- [ ] **Langfuse Action:** Analyze the token usage and cost breakdown per agent using Langfuse Tags.
- [ ] Add a simple evaluation step (e.g., asking the user to score the final report out of 5, and sending that score back to the Langfuse trace).

## Next Steps
Once you review this plan, we can start with **Phase 1** and set up the Python environment and dependencies!
