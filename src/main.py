# src/main.py

import os
import sys
from dotenv import load_dotenv

# --- This import handling block is still required ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
# ----------------------------------------------------

# We now import the ManagerAgent, our new single point of entry.
from src.agents.manager_agent import ManagerAgent

def main():
    """
    The main function to run the multi-agent marketing system.
    """
    load_dotenv()
    
    print("--- Multi-Agent Marketing System Initialized ---")
    
    # Instantiate the Manager Agent
    manager = ManagerAgent()
    
    # A list of different goals to test the manager's delegation logic
    test_goals = [
        "Create an engaging Instagram post about our weekly special.",
        "Check for any new customer reviews and draft responses."
    ]
    
    # Loop through the goals and let the manager delegate each one
    for i, goal in enumerate(test_goals):
        print(f"\n--- Starting Task {i+1}/{len(test_goals)} ---")
        # The main interaction point is now the manager's delegate_task method
        final_result = manager.delegate_task(goal)
        
        print(f"\n--- Task {i+1} Final Output ---")
        print(final_result)
        print("---------------------------------")

if __name__ == "__main__":
    main()