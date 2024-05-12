import os
from flask import Flask, request, jsonify, render_template
import pandas as pd
import requests

app = Flask(__name__)

# Get OpenAI API key from environment variable
api_key = os.getenv('apiKey')

# Function to send file content to OpenAI API
def send_to_openai(content):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        'model': 'text-davinci-002',
        'prompt': content,
        'max_tokens': 50
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Check if a file is uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Check if the file has a valid filename
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read the CSV file using pandas
    try:
        df = pd.read_csv(file)
        # Get content from the CSV file
        content = ' '.join(df.iloc[:, 0].astype(str).tolist())  # Assume first column contains text data
        print("File content:")
        print(content)

        # Additional input from the form
        user_input = request.form.get('input', '')  # Get the 'input' field value from the form
        
        # Combine CSV content with additional input
        combined_content = f"{user_input} {content}"

        # Send combined content to OpenAI API
        openai_response = send_to_openai(combined_content)
        return jsonify(openai_response), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to read or process CSV: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
