import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define the OpenAI API key and project details
OPENAI_API_KEY = os.getenv('apiKey')
OPENAI_ORGANIZATION = "org-fq13CkVOYwvZK7BjeJxqySk1"
OPENAI_PROJECT = "proj_VFmwoRIS4vUBNX20sw0MPHhD"

@app.route('/')
def index():
    print("index")
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    print("a")
    try:
        print("submit")
        # Extract user input from the POST request
        user_input = request.form.get('user_input')
        print("Received user input:", user_input)

        # Prepare the request payload for the OpenAI API
        request_payload = {
            "model": "gpt-3.5-turbo",
        "messages": [{"role": "system","content": "You are a french man"},
                  {"role": "user","content": "Why Sky is blue?"}
                 ],
            "temperature": 0.7
        }

        # Set the headers with Authorization and Content-Type
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
            "OpenAI-Organization": OPENAI_ORGANIZATION,
            "OpenAI-Project": OPENAI_PROJECT
        }

        # Send the POST request to the OpenAI API
        endpoint_url = "https://api.openai.com/v1/chat/completions"
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
