import os
from dotenv import load_dotenv
from core.graph import build_graph
from langfuse.callback import CallbackHandler

load_dotenv()

def main():
    # Check if API keys are set up
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("LANGFUSE_SECRET_KEY"):
        print("Please configure your .env file with OPENAI_API_KEY and Langfuse keys!")
        return

    # Setup Langfuse Callback
    langfuse_handler = CallbackHandler()
    
    graph = build_graph()
    query = "Analyze Apple's (AAPL) current market position based on news and financials."
    
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
