import os
from dotenv import load_dotenv
from agents.social_media_agent import SocialMediaAgent

def main():
    """
    The main function to run the AI Social Media Agent.
    """
    # Load environment variables from the .env file in the project root
    # This is crucial for securely managing API keys.
    load_dotenv()
    
    print("--- AI Social Media Agent Initialized ---")
    
    # Instantiate the agent
    agent = SocialMediaAgent()
    
    # Define a clear, specific goal for the agent's first run
    user_goal = "Create a witty and engaging Instagram post about our weekly special."
    
    # Run the agent with the specified goal
    final_result = agent.run(user_goal)
    
    # Print the final output from the agent
    print("\n--- Agent's Final Output ---")
    print(final_result)
    print("----------------------------")

if __name__ == "__main__":
    # This standard Python construct ensures that the main() function
    # is called only when the script is executed directly.
    main()