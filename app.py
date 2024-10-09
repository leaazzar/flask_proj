from flask import Flask, request, jsonify
from flask_cors import CORS
from db import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Welcome to Lab 5!"

@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))
@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()  # Get JSON data from request
    print("Received data:", user)  # Log received data for debugging
    return jsonify(insert_user(user))  # Insert user into the database


@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))

if __name__ == "__main__":
    create_db_table()  # Ensure table is created
    app.run(debug=True)  # Enable debug mode for detailed error output
