from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        return jsonify({"message": "This is a GET request"})
    elif request.method == 'POST':
        data = request.json
        print(data)  # Parse JSON data from the request body
        return jsonify({"message": "This is a POST request", "data": data})