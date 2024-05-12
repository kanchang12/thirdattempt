import os
import pandas as pd
import requests
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

# Define your Google Cloud project ID and access token
PROJECT_ID = "algebraic-ward-422922-e3"
YOUR_ACCESS_TOKEN = os.getenv('apiKey')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Parse JSON data from the POST request
        data = request.get_json()

        # Extract relevant data from the request (adjust as needed based on your data structure)
        user_input = data.get('user_input')
        location = data.get('location')

        # Prepare the request payload for the Google Cloud AI Platform endpoint
        endpoint_url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/publishers/google/models/gemini-1.0-pro:streamGenerateContent"
        
        request_payload = {
            "contents": [
                {
                    "role": "USER",
                    "parts": [
                        {
                            "text": user_input
                        }
                    ]
                }
            ],
            "systemInstruction": {
                "role": "USER",
                "parts": [
                    {
                        "text": f"Get the weather for {location}"
                    }
                ]
            },
            "tools": [
                {
                    "functionDeclarations": [
                        {
                            "name": "get_current_weather",
                            "description": "Get the current weather in a given location",
                            "parameters": {
                                "location": {
                                    "type": "string",
                                    "description": "Location"
                                }
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.5,
                "topP": 0.9,
                "topK": 50,
                "candidateCount": 1,
                "maxOutputTokens": 100,
                "stopSequences": [],
                "responseMimeType": "text/plain"
            }
        }

       # Set the query parameters with the API key
        params = {
            "key": API_KEY
        }

        # Send the POST request to the Google Cloud AI Platform endpoint with API key
        response = requests.post(endpoint_url, json=request_payload, params=params)

        # Send the POST request to the Google Cloud AI Platform endpoint
        response = requests.post(endpoint_url, json=request_payload, headers=headers)

        # Process the response from the AI Platform endpoint
        if response.status_code == 200:
            result = response.json()
            # Extract and return relevant data from the result as needed
            return jsonify(result), 200
        else:
            return jsonify({'error': f'Request failed with status code {response.status_code}'}), response.status_code

    except Exception as e:
        return jsonify({'error': f'Failed to process request: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
