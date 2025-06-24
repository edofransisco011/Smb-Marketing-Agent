from src.agents.social_media_agent import SocialMediaAgent
from src.agents.reputation_agent import ReputationAgent

class ManagerAgent:
    """
    The ManagerAgent is the orchestrator of the multi-agent system.
    It analyzes the user's goal and delegates the task to the appropriate
    specialist agent.
    """
    def __init__(self, business_profile: str):
        """
        Initializes the ManagerAgent by creating specialist agents and passing
        the dynamic business profile to them.
        """
        print("ManagerAgent: Initializing specialist agents...")
        self.social_media_agent = SocialMediaAgent(business_profile=business_profile)
        self.reputation_agent = ReputationAgent(business_profile=business_profile)
        print("ManagerAgent: Specialists are ready.")

    def delegate_task(self, user_goal: str):
        """
        Analyzes the user's goal using simple keyword matching and routes it 
        to the correct specialist agent.
        """
        print(f"\nManagerAgent: Received goal -> '{user_goal}'. Analyzing...")

        social_keywords = ["post", "instagram", "social media", "tweet", "facebook", "content", "create"]
        reputation_keywords = ["review", "reputation", "feedback", "comment", "rating", "respond"]

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
            print("ManagerAgent: Goal is unclear. Could not delegate to a specialist.")
            return "Error: I'm not sure which specialist should handle this goal. Please be more specific. Try using words like 'post' for social media or 'review' for reputation management."