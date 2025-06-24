import os
from tavily import TavilyClient

def search_local_trends(query: str) -> str:
    """
    Searches the web for local trends, news, or events based on a query.
    
    This tool is used by the AI agent to gather real-time information to make its
    marketing content more relevant and timely. For example, it can search for
    "local events in [city] this weekend" or "trending coffee shop aesthetics 2025".

    Args:
        query: The search query string.

    Returns:
        A string containing the summarized search results, or an error message.
    """
    try:
        # Retrieve the API key from environment variables
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY is not set."

        # Initialize the Tavily client
        tavily = TavilyClient(api_key=api_key)

        # Perform the search and get a simple, summarized result
        # include_answer=True gives a direct answer to the query if possible.
        response = tavily.search(query=query, search_depth="basic", include_answer=True)
        
        # We'll return the 'answer' if it exists, otherwise the main results.
        # This gives the LLM the most concise information to work with.
        return response.get('answer', str(response['results']))

    except Exception as e:
        # Return a structured error message if the search fails
        return f"Error performing search for query '{query}': {e}"

# --- Tool Schema ---
# This dictionary describes the tool to the LLM. It explains what the tool
# does, what parameters it takes, and what type those parameters are.
# This is crucial for the LLM to correctly generate the function call.
search_local_trends_schema = {
    "type": "function",
    "function": {
        "name": "search_local_trends",
        "description": "Searches the web for local trends, news, or events to get inspiration for marketing content.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The specific search query, e.g., 'coffee shop promotions for students'."
                }
            },
            "required": ["query"]
        }
    }
}