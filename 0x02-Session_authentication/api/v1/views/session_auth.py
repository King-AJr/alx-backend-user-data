#!/usr/bin/env python3
""" Module of Session related views
"""
from os import getenv
from api.v1.views import app_views
from typing import Dict
from flask import abort, jsonify, request, session
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_login():
    """
    Handles user session login.

    Validates the provided email and password, searches for the user,
    and if valid, creates a session and sets a session cookie.

    Returns:
        Response: A JSON response containing user data on successful login,
                or an error response if login fails.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if email is missing
    if email is "" or email is None:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing
    if password is "" or password is None:
        return jsonify({"error": "password missing"}), 400

    # Search for users with the provided email
    users = User.search({"email": email})

    # If no users found or the list is empty, return an error
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    # Iterate through the list of users to check if the password is valid
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth

            session_id = auth.create_session(user.id)
            cookie_name = getenv("SESSION_NAME")

            # Create a JSON response with user data
            response = jsonify(user.to_json())

            # Set the session cookie in the response
            response.set_cookie(cookie_name, session_id)

            return response
        else:
            return jsonify({"error": "wrong password"}), 401

    # If no user with valid credentials is found, return None
    return None
