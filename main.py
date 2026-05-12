import os
import argparse
from dotenv import load_dotenv
from core.graph import build_graph
from langfuse.callback import CallbackHandler

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Run the Financial Analyst Swarm.")
    parser.add_argument(
        "query", 
        nargs="?", 
        default="Analyze Apple's (AAPL) current market position based on news and financials.",
        help="The research query for the swarm."
    )
    args = parser.parse_args()

    # Check if API keys are set up
    required_keys = ["OPENAI_API_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_PUBLIC_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"Missing required environment variables: {', '.join(missing_keys)}")
        print("Please configure them in your .env file!")
        return

    # Setup Langfuse Callback
    langfuse_handler = CallbackHandler()
    
    graph = build_graph()
    query = args.query
    
    print(f"User Query: {query}\n")
    print("--- Execution Started ---")
    
    # Execute the graph with the Langfuse handler
    config = {"callbacks": [langfuse_handler]}
    initial_state = {"query": query}
    
    # We use stream so we can see the progress of the map-reduce
    for s in graph.stream(initial_state, config=config):
        print("\n--- Current State Update ---")
        for node_name, state_update in s.items():
            print(f"Node '{node_name}' finished.")
            if node_name == "supervisor":
                print(f"Assigned Tasks: {state_update.get('tasks')}")
            elif node_name in ["news_analyst", "quant_analyst"]:
                completed = state_update.get("completed_tasks", [])
                for t in completed:
                    print(f"-> Completed {t['task_type']} task for {t['ticker']}")
            elif node_name == "synthesizer":
                print("\n--- FINAL INVESTMENT MEMO ---\n")
                print(state_update.get("final_report"))
                
    # Flush Langfuse telemetry
    langfuse_handler.flush()
    print("\n--- Execution Completed ---")
    print("Check the trace in your Langfuse Dashboard!")

if __name__ == "__main__":
    main()
