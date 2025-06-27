from flask import request, jsonify, g
import jwt
from functools import wraps
import os

def authenticate_user(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({
                    "status": "error",
                    "message": "Invalid token",
                    "data": [],
                    "errors": ["Token is invalid or expired, please login to get a new token"],
                }), 401

            token = auth_header.split(" ")[1]

            try:
                decoded = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])

                user_role = decoded.get("role")
                if user_role == "admin" or user_role in allowed_roles:
                    g.user = decoded
                    return f(*args, **kwargs)
                else:
                    return jsonify({
                        "status": "error",
                        "message": "Access denied",
                        "data": [],
                        "errors": [f"User role must be one of {allowed_roles} and you are {user_role}"],
                    }), 403

            except jwt.ExpiredSignatureError as err:
                return jsonify({
                    "status": "error",
                    "message": "The token has expired. Please log in again",
                    "data": [],
                    "errors": [str(err)],
                }), 401
            except jwt.InvalidTokenError as err:
                return jsonify({
                    "status": "error",
                    "message": "Invalid token. Please log in or provide a valid token",
                    "data": [],
                    "errors": [str(err)],
                }), 401
            except Exception as err:
                return jsonify({
                    "status": "error",
                    "message": "An unexpected error occurred while trying to verify the token",
                    "data": [],
                    "errors": [str(err)],
                }), 500

        return wrapper
    return decorator