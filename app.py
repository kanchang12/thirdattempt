import os
from flask import Flask, request, jsonify, render_template
import openai
import pandas as pd
import json
from system_instruction import load_context_data



app = Flask(__name__)

# Define the OpenAI API key
OPENAI_API_KEY = os.getenv('apiKey')
openai.api_key = OPENAI_API_KEY

@app.route('/')
def index():
    return render_template('index.html')


context_data = load_context_data()

@app.route('/submit', methods=['POST'])
def submit():
    print("In function")
    try:
        csv_file = request.files.get('csv_content')

        if not csv_file:
            return "No file uploaded", 400

        # Get the filename from the uploaded file object
        filename = csv_file.filename  

        # Process the uploaded CSV file with pandas (using filename)
        try:
            df = pd.read_csv(csv_file)  # Can access the file using the filename
            csv_string = df.to_string()
            print(csv_string)
            # Retrieve user input from the form data
            user_input = request.form.get('user_input')
            print(user_input)
            prompt = csv_string + user_input

            # Prepare the chat completion request to OpenAI
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": context_data},
                    {"role": "user", "content": prompt}  # Passing DataFrame 'df' directly is not supported
                ]
            )

            # Extract the response message content
            response_content = completion['choices'][0]['message']['content']

            print(response_content)

            # Return the response in JSON format
            return jsonify({'response': response_content}), 200

        except Exception as e:
            print(f"Error processing CSV: {e}")
            return "Error processing CSV file", 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


