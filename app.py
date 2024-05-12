import os
import pandas as pd
import requests
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

# Define your Google Cloud project ID and access token
#PROJECT_ID = "algebraic-ward-422922-e3"
YOUR_ACCESS_TOKEN = os.getenv('apiKey')
print(YOUR_ACCESS_TOKEN)

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

        # Send request to OpenAI Chat Completion API
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Why Sku is blue?"}
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
