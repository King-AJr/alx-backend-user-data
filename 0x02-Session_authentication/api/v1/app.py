#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_status = getenv("AUTH_TYPE")
if auth_status == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_status == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_status == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Error handler for error 401
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Error handler for error 403
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
    before request is dealt with check if;
    authentication is required, if authentication
    is required reply with the correct status code and
    message
    """
    if auth is None:
        pass
    else:
        setattr(request, "current_user", auth.current_user(request))
        excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                          '/api/v1/forbidden/']
        cookie = auth.session_cookie(request)
        if auth.require_auth(request.path, excluded_paths):
            if auth.authorization_header(request) is None and cookie is None:
                error_msg = jsonify({"error": "Unauthorized"})
                abort(401, error_msg)
            if auth.current_user(request) is None:
                error_msg = jsonify({"errors": "Forbidden"})
                abort(403, error_msg)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
