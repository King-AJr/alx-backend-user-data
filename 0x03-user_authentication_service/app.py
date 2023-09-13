#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def hello():
    """
    return french message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """
    Register a user based on form data and handle registration errors.

    This function extracts 'email' and 'password' from a form submitted
    in a request, attempts to register a new user with the provided email
    and password, and handles registration errors, such as duplicate email
    addresses.

    Returns:
        JSON response with appropriate status code and messages.
    """
    # Extract 'email' and 'password' from the submitted form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Print the extracted email and password for debugging purposes
    print(email, password)

    try:
        # Attempt to register a new user with the provided email and password
        AUTH.register_user(email, password)

        # If registration is successful, return a JSON response with success
        # message
        return jsonify({"email": "{}".format(email),
                        "message": "user created"}), 200
    except ValueError:
        # If a ValueError is raised (e.g., due to a duplicate email), return an
        # error response
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
