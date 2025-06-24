# src/agents/reputation_agent.py

import os
import json
from openai import OpenAI
from src.tools.reviews_api import get_latest_reviews, get_latest_reviews_schema

class ReputationAgent:
    """
    The ReputationAgent is a specialized AI agent that monitors and manages
    the business's online reputation by responding to customer reviews.
    """
    def __init__(self):
        """
        Initializes the agent, loading credentials and setting up the client.
        """
        self.client = OpenAI(
            api_key=os.getenv("QWEN_API_KEY"),
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
        )
        self.business_profile = self._load_business_profile()
        # This agent's toolkit is simple: it can only get reviews.
        self.tools = [get_latest_reviews_schema]
        self.tool_dispatcher = {
            "get_latest_reviews": get_latest_reviews,
        }

    def _load_business_profile(self):
        """Loads the business profile from the data directory."""
        try:
            with open("data/business_profile.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "Error: Business profile not found."

    def run(self, user_goal: str):
        """
        The main execution loop for the agent. It fetches reviews, analyzes
        them, and drafts appropriate responses.
        """
        system_prompt = f"""
        You are a professional and empathetic AI Reputation Manager named 'Echo'.
        Your client is a local small business. Here is their profile:
        ---
        {self.business_profile}
        ---
        Your primary goal is to manage the business's online reputation by drafting responses to customer reviews.
        You must operate within the brand voice: '{self.business_profile.split('brand_voice: ')[1].splitlines()[0]}'.

        - For positive reviews (4-5 stars), be thankful and highlight something specific they mentioned.
        - For negative reviews (1-3 stars), be professional, apologize for the poor experience, and offer a way to make it right (e.g., "contact us at..."). Do not be defensive.

        You must first use the `get_latest_reviews` tool to fetch the reviews.
        Then, provide a drafted response for each review you've analyzed.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_goal}
        ]
        
        print(f"🤖 Reputation Agent starting with goal: '{user_goal}'")

        # --- The Agent's Core Thinking Loop ---
        for _ in range(5):
            print("🤔 Reputation Agent is thinking...")
            response = self.client.chat.completions.create(
                model="qwen-max",
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                print("🛠️ Reputation Agent decided to use a tool.")
                messages.append(response_message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = self.tool_dispatcher.get(function_name)
                    
                    if function_to_call:
                        print(f"   - Calling function: {function_name}")
                        function_response = function_to_call() # No arguments needed
                        print(f"   - Function response received.")
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )
                    else:
                        print(f"   - Error: Agent tried to call an unknown function: {function_name}")
                continue
            else:
                print("✅ Reputation Agent finished generating the final response.")
                final_response = response_message.content
                return final_response
        
        return "Error: Agent could not complete the goal within the iteration limit."