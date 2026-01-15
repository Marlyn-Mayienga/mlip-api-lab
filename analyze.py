import json
import os
from typing import Any, Dict
from litellm import completion

# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"

# Read .env file manually
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.startswith("GROQ_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
                os.environ["GROQ_API_KEY"] = api_key

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions
    """
    # implement litellm call here to generate a structured travel itinerary for the given destination
    response = completion(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """You are a professional travel agent with over 10 years of experience. 
                You must respond with valid JSON only using this exact structure:
                {
                    "destination": "string",
                    "price_range": "string",
                    "ideal_visit_times": ["array of strings"],
                    "top_attractions": ["array of strings"]
                }"""
            },
            {
                "role": "user",
                "content": f"Create a travel itinerary for {destination}. Include the price range, ideal times to visit, and top attractions."
            }
        ],
        response_format={"type": "json_object"},
        api_key=api_key
    )

        
    # extract the json content from the response
    content = response.choices[0].message.content

    # Parse the JSON content
    data = json.loads(content)
    # See https://docs.litellm.ai/docs/ for reference.    

    return data
