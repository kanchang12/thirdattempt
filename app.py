from flask import Flask, request, jsonify
import pandas as pd
import io

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is the homepage!"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    user_input = data['input']
    
    # Check if a file is uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # Check if the file has a valid filename
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read the CSV file using pandas
    try:
        df = pd.read_csv(io.StringIO(file.stream.read().decode('utf-8')))
        print("CSV file contents:")
        print(df.head())  # Optionally print the CSV content
    except Exception as e:
        return jsonify({'error': f'Failed to read CSV: {str(e)}'}), 400

    # Process the user_input and CSV data further here

    # Sending a response back to the JavaScript (optional)
    response = {'message': 'Data received and processed successfully'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
