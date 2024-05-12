from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is the homepage!"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    user_input = data['input']
    
    # Here you can process the user_input variable (e.g., print or return a response)
    print(f"Received user input: {user_input}")

    # Sending a response back to the JavaScript (optional)
    response = {'message': 'Data received successfully'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
