import os
import json
from openai import OpenAI
from src.tools.web_search import search_local_trends, search_local_trends_schema
from src.tools.social_api import post_to_instagram, post_to_instagram_schema

class SocialMediaAgent:
    """
    The SocialMediaAgent is a specialized AI agent responsible for creating
    and managing social media content for a local SMB.
    """
    def __init__(self, business_profile: str):
        """
        Initializes the agent with a dynamic business profile.
        """
        self.client = OpenAI(
            api_key=os.getenv("QWEN_API_KEY"),
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
        self.business_profile = business_profile
        self.tools = [search_local_trends_schema, post_to_instagram_schema]
        self.tool_dispatcher = {
            "search_local_trends": search_local_trends,
            "post_to_instagram": post_to_instagram
        }

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
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_goal}
        ]
        
        print(f"🤖 Agent starting with goal: '{user_goal}'")

        for _ in range(5):
            print("🤔 Agent is thinking...")
            response = self.client.chat.completions.create(
                model="qwen-max",
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                print("🛠️ Agent decided to use a tool.")
                messages.append(response_message)
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = self.tool_dispatcher.get(function_name)
                    if function_to_call:
                        function_args = json.loads(tool_call.function.arguments)
                        print(f"   - Calling function: {function_name} with args: {function_args}")
                        function_response = function_to_call(**function_args)
                        print(f"   - Function response: {function_response}")
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
                print("✅ Agent finished generating the final response.")
                final_response = response_message.content
                return final_response
        return "Error: Agent could not complete the goal within the iteration limit."