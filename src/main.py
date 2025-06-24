import os
import sys
from dotenv import load_dotenv

# --- Fix for ModuleNotFoundError ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
# ------------------------------------

from src.agents.social_media_agent import SocialMediaAgent

def main():
    """
    The main function to run the AI Social Media Agent.
    """
    load_dotenv()
    
    # --- TEMPORARY DEBUG LINE ---
    # Let's print the key to see if it's being loaded. We'll remove this later.
    print(f"DEBUG: Loaded QWEN_API_KEY: {os.getenv('QWEN_API_KEY')}")
    # ----------------------------

    print("\n--- AI Social Media Agent Initialized ---")
    
    agent = SocialMediaAgent()
    
    user_goal = "Create a witty and engaging Instagram post about our weekly special."
    
    final_result = agent.run(user_goal)
    
    print("\n--- Agent's Final Output ---")
    print(final_result)
    print("----------------------------")

if __name__ == "__main__":
    main()