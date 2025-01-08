from flask import Flask, jsonify, request
import json
import logging

app = Flask(__name__)

# Load user data from an external JSON file
with open('mock_users.json', 'r') as f:
    mock_users = json.load(f)["users"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    """
    Logs the user in with email + password.
    On success, returns the user object (excluding sensitive fields),
    on error, returns 400 and JSON with an error field.
    """
    input_data = request.json or {}
    email = input_data.get('email')
    password = input_data.get('password')

    # Check for missing input
    if not email or not password:
        return jsonify({"error": "Missing input"}), 400

    # Simulate database query from external data
    user = mock_users.get(email)

    # Validate user and password
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid login credentials"}), 400

    # Simulate session creation (for demonstration only)
    session = {"user_id": user["id"], "remember": input_data.get("remember", True)}

    # Log the successful login
    logger.info(f"LOGIN OK: User '{email}' logged in successfully. Agent: {request.headers.get('User-Agent')}")

    # Exclude sensitive fields like password before returning user info
    user_response = {key: value for key, value in user.items() if key != "password"}
    return jsonify(user_response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
