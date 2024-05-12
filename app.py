import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Define the OpenAI API key
OPENAI_API_KEY = os.getenv('apiKey')
openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get user input from the form
        user_input = request.form.get('user_input')

        # Prepare the chat completion request to OpenAI
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        # Extract the response message content
        response_content = completion['choices'][0]['message']['content']

        # Return the response in JSON format
        return jsonify({'response': response_content}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
