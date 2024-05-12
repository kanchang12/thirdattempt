import os
import pandas as pd
import requests
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

# Define your Google Cloud project ID and access token
PROJECT_ID = "algebraic-ward-422922-e3"
YOUR_ACCESS_TOKEN = os.getenv('apiKey')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Parse JSON data from the POST request
        data = request.get_json()

        # Extract relevant data from the request
        user_input = data.get('user_input')

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
                        "fileData": {
                            "mimeType": "text/plain",
                            "fileUri": "https://gist.githubusercontent.com/kanchang12/509b21ef02ab5aefa526b956925423b7/raw/f2dc0569a96b9b4658e38486caefbd19f3572fb7/system_instruction.txt"
                        }
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

        # Send the POST request to the Google Cloud AI Platform endpoint
        response = requests.post(endpoint_url, json=request_payload)

        # Process the response from the AI Platform endpoint
        if response.status_code == 200:
            result = response.json()
            return jsonify(result), 200
        else:
            return jsonify({'error': f'Request failed with status code {response.status_code}'}), response.status_code

    except Exception as e:
        return jsonify({'error': f'Failed to process request: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)
