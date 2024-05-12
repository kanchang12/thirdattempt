import os
import requests
from flask import Flask, request, jsonify, render_template
import openai
import json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Define the OpenAI API key and project details
OPENAI_API_KEY = os.getenv('apiKey')
print(OPENAI_API_KEY)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    completion = client.chat.completions.create(model="gpt-3.5-turbo-16k",
                                                messages=[
                                                    {"role": "system", "content": "You are a helpful assistant."},
                                                    {"role": "user", "content": "Hello!"}
                                                ]
                                               )
    response = completion.choices[0].message
    print(completion.choices[0].message)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
