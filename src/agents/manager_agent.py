# src/agents/manager_agent.py

from src.agents.social_media_agent import SocialMediaAgent
from src.agents.reputation_agent import ReputationAgent

class ManagerAgent:
    """
    The ManagerAgent is the orchestrator of the multi-agent system.
    It analyzes the user's goal and delegates the task to the appropriate
    specialist agent.
    """
    def __init__(self):
        """
        Initializes the ManagerAgent by creating instances of the specialist 
        agents it oversees.
        """
        print("ManagerAgent: Initializing specialist agents...")
        self.social_media_agent = SocialMediaAgent()
        self.reputation_agent = ReputationAgent()
        print("ManagerAgent: Specialists are ready.")

    def delegate_task(self, user_goal: str):
        """
        Analyzes the user's goal using simple keyword matching and routes it 
        to the correct specialist agent.

        Args:
            user_goal: The high-level goal provided by the user.

        Returns:
            The result from the specialist agent's execution.
        """
        print(f"\nManagerAgent: Received goal -> '{user_goal}'. Analyzing...")

        # --- Simple & Robust Keyword-Based Routing ---
        # This is an efficient method for delegation in systems with clearly defined roles.
        social_keywords = ["post", "instagram", "social media", "tweet", "facebook", "content", "create"]
        reputation_keywords = ["review", "reputation", "feedback", "comment", "rating", "respond"]

        # Convert goal to lowercase for case-insensitive matching
        goal_lower = user_goal.lower()

        is_social_task = any(keyword in goal_lower for keyword in social_keywords)
        is_reputation_task = any(keyword in goal_lower for keyword in reputation_keywords)

        if is_social_task:
            print("ManagerAgent: Goal identified for Social Media. Delegating to 'Spark'...")
            return self.social_media_agent.run(user_goal)
        
        elif is_reputation_task:
            print("ManagerAgent: Goal identified for Reputation. Delegating to 'Echo'...")
            return self.reputation_agent.run(user_goal)

        else:
            # Fallback for unclear or unsupported goals
            print("ManagerAgent: Goal is unclear. Could not delegate to a specialist.")
            return "Error: I'm not sure which specialist should handle this goal. Please be more specific. Try using words like 'post' for social media or 'review' for reputation management."