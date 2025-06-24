import os
import json
from openai import OpenAI
# NEW - Explicitly tells Python to look inside the 'src' folder
from src.tools.web_search import search_local_trends, search_local_trends_schema
from src.tools.social_api import post_to_instagram, post_to_instagram_schema
class SocialMediaAgent:
    """
    The SocialMediaAgent is a specialized AI agent responsible for creating
    and managing social media content for a local SMB.
    """
    def __init__(self):
        """
        Initializes the agent, loading credentials and setting up the client.
        """
        # We point the OpenAI client to the Alibaba Cloud Dashscope endpoint.
        self.client = OpenAI(
            api_key=os.getenv("QWEN_API_KEY"),
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
        # Load the business profile to provide context to the agent
        self.business_profile = self._load_business_profile()
        # Define the tools the agent has access to
        self.tools = [search_local_trends_schema, post_to_instagram_schema]
        # A mapping from tool name to the actual Python function
        self.tool_dispatcher = {
            "search_local_trends": search_local_trends,
            "post_to_instagram": post_to_instagram
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
        The main execution loop for the agent.
        It takes a user's goal and works to achieve it by thinking,
        using tools, and generating content.
        """
        system_prompt = f"""
        You are a highly skilled, autonomous AI Social Media Manager named 'Spark'.
        Your client is a local small business. Here is their profile:
        ---
        {self.business_profile}
        ---
        Your primary goal is to help this business thrive by creating engaging social media content.
        You are proactive and creative. You must operate within the brand voice defined in the profile.

        You have access to a set of tools to help you. When you need to use a tool,
        respond ONLY with the appropriate JSON object to call the function.
        Do not add any other text or explanation.

        If you have enough information to generate the post directly, do that.
        Your final output should be the complete, ready-to-post content.
        """

        # Initialize the conversation history
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_goal}
        ]
        
        print(f"🤖 Agent starting with goal: '{user_goal}'")

        # --- The Agent's Core Thinking Loop ---
        for _ in range(5): # Limit to 5 iterations to prevent infinite loops
            print("🤔 Agent is thinking...")
            response = self.client.chat.completions.create(
                model="qwen-max",
                messages=messages,
                tools=self.tools,
                tool_choice="auto" # The model decides whether to use a tool
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # --- Step 1: Check if the model wants to use a tool ---
            if tool_calls:
                print("🛠️ Agent decided to use a tool.")
                # Append the assistant's response to the message history
                messages.append(response_message) 

                # --- Step 2: Execute the chosen tool(s) ---
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = self.tool_dispatcher.get(function_name)
                    
                    if function_to_call:
                        function_args = json.loads(tool_call.function.arguments)
                        print(f"   - Calling function: {function_name} with args: {function_args}")
                        
                        # Call the actual Python function
                        function_response = function_to_call(**function_args)
                        print(f"   - Function response: {function_response}")

                        # Append the tool's output to the message history
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
                
                # Loop continues to the next thinking step with the new tool context
                continue

            # --- Step 3: If no tool is used, the response is the final answer ---
            else:
                print("✅ Agent finished generating the final response.")
                final_response = response_message.content
                return final_response
        
        return "Error: Agent could not complete the goal within the iteration limit."