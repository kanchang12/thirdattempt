import os
import pandas as pd
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# API endpoint details
api_url = "https://api.vertexai.cloud/v1/generative-models/models/gemini-1.0-pro-001:generateContent"
api_key = os.getenv('apiKey')  # Replace with your API key

def process_csv_data(csv_data):
    try:
        # Convert CSV data to DataFrame
        df = pd.read_csv(csv_data)

        # Perform any necessary data processing here (e.g., cleaning, transformation)

        # Example: Send processed data to API
        response = requests.post(api_url, json=df.to_dict(orient='records'), headers={'Authorization': f'Bearer {api_key}'})
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'API request failed with status code {response.status_code}'}

    except Exception as e:
        return {'error': f'Error processing CSV data: {str(e)}'}

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Check if a file is uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        # Check if the file has a valid filename
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Read the CSV file content
        csv_data = file.read()

        # Process the CSV data and send to API
        result = process_csv_data(csv_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': f'Failed to process request: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
