def post_to_instagram(caption: str, image_description: str) -> str:
    """
    Posts content to a mock Instagram account.

    In a real application, this would interact with the Instagram Graph API.
    For this project, it simulates the action by printing the content to the
    console. This allows us to test the agent's ability to use the tool
    without needing real credentials or making live posts.

    Args:
        caption: The text content for the Instagram post.
        image_description: A detailed description of the image to be generated or posted.
                           This helps the agent think about the visual aspect of the post.

    Returns:
        A string confirming the successful simulation of the post.
    """
    print("--- MOCK INSTAGRAM POST ---")
    print(f"IMAGE: {image_description}")
    print(f"CAPTION: {caption}")
    print("---------------------------")
    
    return "Success: The post was successfully sent to the mock Instagram API."

# --- Tool Schema ---
# Describes the mock Instagram tool to the LLM.
post_to_instagram_schema = {
    "type": "function",
    "function": {
        "name": "post_to_instagram",
        "description": "Creates a new post on the business's Instagram account.",
        "parameters": {
            "type": "object",
            "properties": {
                "caption": {
                    "type": "string",
                    "description": "The full text of the post's caption, including hashtags."
                },
                "image_description": {
                    "type": "string",
                    "description": "A detailed, descriptive prompt for an AI image generator to create the post's visual."
                }
            },
            "required": ["caption", "image_description"]
        }
    }
}