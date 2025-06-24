# src/tools/reviews_api.py

def get_latest_reviews() -> str:
    """
    Retrieves the latest customer reviews from a mock database.

    In a real application, this would fetch data from platforms like
    Google Maps, Yelp, etc. For this project, it returns a hardcoded
    JSON string of sample reviews to simulate the API response. This allows
    the Reputation Agent to have consistent data to work with.

    Returns:
        A JSON string containing a list of recent customer reviews.
    """
    print("--- MOCK REVIEWS API ---")
    print("   - Fetching latest customer reviews...")
    
    # A hardcoded list of reviews to simulate a real API response.
    mock_reviews = [
        {
            "author": "Alice",
            "rating": 5,
            "comment": "The 'Volcano' Dark Roast is absolutely life-changing! The atmosphere is so cozy and the staff are incredibly friendly. My new favorite spot!"
        },
        {
            "author": "Bob",
            "rating": 4,
            "comment": "Great coffee and fast Wi-Fi. It can get a little crowded during peak hours, but it's a solid place to work from."
        },
        {
            "author": "Charlie",
            "rating": 2,
            "comment": "The pastries were a bit stale and my latte was lukewarm. Was really hoping for more. Disappointed."
        }
    ]
    
    # We return the reviews as a JSON string, as this is a common
    # format for API responses and easy for the LLM to parse.
    import json
    return json.dumps(mock_reviews)

# --- Tool Schema ---
# This describes the tool to the LLM. Notice it has no parameters,
# as it always fetches the latest reviews by default.
get_latest_reviews_schema = {
    "type": "function",
    "function": {
        "name": "get_latest_reviews",
        "description": "Fetches the most recent customer reviews for the business from online platforms.",
        "parameters": {
            "type": "object",
            "properties": {}, # No parameters needed for this tool
            "required": []
        }
    }
}