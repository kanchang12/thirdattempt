import os
import pandas as pd
import requests
from flask import Flask, request, jsonify, render_template
from openai import OpenAI


app = Flask(__name__)

# Retrieve the OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv('apiKey')
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=OPENAI_API_KEY)
print(OPENAI_API_KEY)



@app.route('/')
def index():
    print('index')
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Extract user input from the POST request
        user_input = request.form['user_input']
        print(user_input)

        # Send request to OpenAI Chat Completion API with Authorization header
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "why Sky is blue?"}
            ]
        )

        # Extract the response content from the API response
        if completion and completion.choices:
            response_content = completion.choices[0].message.get('content', '')

            # Return the response content as JSON
            return jsonify({'response': response_content}), 200

        return jsonify({'error': 'Failed to get valid response from OpenAI'}), 500

    except Exception as e:
        return jsonify({'error': f'Failed to process request: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(debug=True)
