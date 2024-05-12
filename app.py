import os
import requests
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

def process_user_input(user_input):
    try:
        # Define the API key and API endpoint
        api_key = os.getenv('apiKey')  # Replace with your API key
        endpoint = "https://api.vertexai.cloud/v1/generative-models/models/gemini-1.0-pro-001:generateContent"

        # Define the user's prompt in a Content object
        user_prompt_content = Content(
            role="user",
            parts=[
                Part.from_text(user_input),
            ],
        )

        # Define a function declaration for an API request
        function_name = "get_current_weather"
        get_current_weather_func = FunctionDeclaration(
            name=function_name,
            description="Get the current weather in a given location",
            parameters={
                "type": "object",
                "properties": {"location": {"type": "string", "description": "Location"}},
            },
        )

        # Create a Tool including the function declaration
        weather_tool = Tool(
            function_declarations=[get_current_weather_func],
        )

        # Construct the request payload
        payload = {
            "content": user_prompt_content.to_dict(),
            "generationConfig": {"temperature": 0},
            "tools": [weather_tool.to_dict()],
        }

        # Send the request to the API endpoint with the API key in the headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        response = requests.post(endpoint, json=payload, headers=headers)

        # Extract the model response from the API response
        if response.status_code == 200:
            model_response = response.json()
            return model_response.get("text", "No response text available")
        else:
            return f"Error: API request failed with status code {response.status_code}"

    except Exception as e:
        return f"Error: {str(e)}"
