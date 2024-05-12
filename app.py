from flask import Flask, request, jsonify
import pandas as pd
import io

app = Flask(__name__)

# Dummy function to simulate processing of CSV data
def process_data(data):
    # Example: Calculate sum of a column
    total_sum = data['Amount'].sum()
    return total_sum

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

        # Process the CSV data
        result = process_data(df)
        response = {'message': f'Data received and processed successfully. Total sum: {result}'}
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to read or process CSV: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
