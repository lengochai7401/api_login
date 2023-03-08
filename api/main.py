import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from dotenv import set_key

app = Flask(__name__)
load_dotenv()

# Load user accounts from environment
USER_ACCOUNTS = [
    {'id': 1, 'username': os.getenv('ADMIN_USERNAME'), 'password': os.getenv(
        'ADMIN_PASSWORD'), 'ip_address': os.getenv('ADMIN_IP_ADDRESS')},
    {'id': 2, 'username': os.getenv('USER1_USERNAME'), 'password': os.getenv(
        'USER1_PASSWORD'), 'ip_address': os.getenv('USER1_IP_ADDRESS')},
    {'id': 3, 'username': os.getenv('USER2_USERNAME'), 'password': os.getenv(
        'USER2_PASSWORD'), 'ip_address': os.getenv('USER2_IP_ADDRESS')},
    # Add more user accounts as needed
]


@app.route('/')
def home():
    return "Hello world"


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Check if the username and password match any user account
    for account in USER_ACCOUNTS:
        if username == account['username'] and password == account['password']:
            # Login successful, return the user data as a JSON response
            user_data = {
                'id': account['id'],
                'username': username,
                'ip_address': account.get('ip_address'),
                # Add other user data fields as needed
            }
            return jsonify(user_data)

    # Login failed, return an error response
    error_data = {
        'error': 'Invalid username or password'
    }
    return jsonify(error_data), 401  # Unauthorized status code


@app.route('/api/update_user_data/<int:user_id>', methods=['PUT'])
def update_user_data(user_id):
    # Check if the user ID is valid
    user_account = next(
        (account for account in USER_ACCOUNTS if account['id'] == user_id), None)
    if not user_account:
        error_data = {
            'error': 'User account not found'
        }
        return jsonify(error_data), 404  # Not found status code

    # Check if the request contains the new IP address
    new_ip_address = request.json.get('ip_address', None)
    if new_ip_address:
        user_account['ip_address'] = new_ip_address
        set_key(
            '.env', f"{user_account['username'].upper()}_IP_ADDRESS", new_ip_address)

    # Return the updated user data as a JSON response
    user_data = {
        'id': user_account['id'],
        'username': user_account['username'],
        'ip_address': user_account.get('ip_address', None),
        # Add other user data fields as needed
    }
    return jsonify(user_data)


app.run()
