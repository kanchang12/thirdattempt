import os
import requests
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# Define the OpenAI API key
OPENAI_API_KEY = os.getenv('apiKey')
print(OPENAI_API_KEY)

@app.route('/')
def index():
    print(index)
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Extract user input from the POST request
        user_input = request.form.get('user_input')
        print("user input")
        print(user_input)

        # Define the OpenAI endpoint URL
        endpoint_url = "https://api.openai.com/v1/chat/completions"

        # Prepare the request payload for the OpenAI API
        request_payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_input}],
            "temperature": 0.7
        }

        # Set the headers with Authorization and Content-Type
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        # Send the POST request to the OpenAI API
        response = requests.post(endpoint_url, json=request_payload, headers=headers)

        # Process the response from the OpenAI API
        if response.status_code == 200:
            result = response.json()
            if result.get('choices'):
                response_content = result['choices'][0]['message'].get('content', '')
                return jsonify({'response': response_content}), 200
            else:
                return jsonify({'error': 'No valid response from OpenAI'}), 500
        else:
            return jsonify({'error': f'Request failed with status code {response.status_code}'}), response.status_code

    except Exception as e:
        return jsonify({'error': f'Failed to process request: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
