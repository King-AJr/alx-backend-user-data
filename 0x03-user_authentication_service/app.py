#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def hello():
    """
    return french message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
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
    email = request.form.get("email")
    password = request.form.get("password")
    if (
        email is None
        or email == ""
        or not isinstance(email, str)
        or password is None
        or password == ""
        or not isinstance(password, str)
    ):
        raise ValueError

    try:
        # Attempt to register a new user with the provided email and password
        AUTH.register_user(email, password)

        # If registration is successful, return a JSON
        # response with success message
        return jsonify({"email": "{}".format(email),
                        "message": "user created"}), 200
    except ValueError:
        # If a ValueError is raised (e.g., due to a duplicate email), return an
        # error response
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    function that logs user into the server and
    returns a session id
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if (
        email is None
        or email == ""
        or not isinstance(email, str)
        or password is None
        or password == ""
        or not isinstance(password, str)
    ):
        raise ValueError
    auth_status = AUTH.valid_login(email, password)
    if auth_status:
        cookie_value = AUTH.create_session(email)
        cookie_key = "session_id"
        response = jsonify({"email": "{}".format(email),
                            "message": "logged in"})
        # Set the session cookie in the response
        response.set_cookie(cookie_key, cookie_value)

        return response
    else:
        abort(401)


# task 14 - install requests package
@app.route("/sessions", methods=["DELETE"])
def logout():
    cookie_value = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(cookie_value)
    if user:
        del user.session_id
        return redirect('/')
    else:
        abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    cookie_value = request.cookies.get("session_id")
    print("session_id", cookie_value)
    user = AUTH.get_user_from_session_id(cookie_value)

    if user:
        response = jsonify({"email": "{}".format(user.email)}), 200
        return response
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify(
            {"email": "{}".format(email), "reset_token":
             "{}".format(reset_token)}
        )
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    email = request.form.get("email")
    new_password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")
    if email is None or new_password is None or reset_token is None:
        abort(403)
    try:
        print(reset_token, new_password)
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": "{}".format(email),
                        "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
