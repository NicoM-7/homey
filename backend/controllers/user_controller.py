import os
import jwt
import bcrypt
from flask import g, request, jsonify
from sqlalchemy.exc import SQLAlchemyError, DataError, StatementError
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator
from smtplib import SMTPException
from models import User
from db import db
from mail import send_email
from datetime import datetime, timedelta

def get_users():
    try:
        # Copy query parameters and remove restricted keys
        filters = dict(request.args)
        filters.pop("password", None)
        filters.pop("email", None)

        try:
            # Query matching users
            users = User.query.filter_by(**filters).all()
        except (DataError, StatementError) as e:
            return jsonify({
                "status": "error",
                "message": "Invalid query parameter(s)",
                "data": [],
                "errors": [str(e)]
            }), 400

        if not users:
            return jsonify({
                "status": "error",
                "message": "No user(s) found",
                "data": [],
                "errors": [f"No user(s) found with data {filters}"]
            }), 404

        # Exclude email and password in serialized output
        result = [user.to_safe_dict() for user in users]

        return jsonify({
            "status": "success",
            "message": f"{len(result)} user(s) found",
            "data": result,
            "errors": []
        }), 200

    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to get user(s)",
            "data": [],
            "errors": [str(err)]
        }), 500

def get_user_by_id(id):
    try:
        # Ensure the ID is valid (in case routing doesn't enforce int)
        if not isinstance(id, int):
            return jsonify({
                "status": "error",
                "message": f"Invalid user ID: {id}",
                "data": [],
                "errors": [f"User ID '{id}' must be an integer"]
            }), 400

        user = User.query.get(id)

        if not user:
            return jsonify({
                "status": "error",
                "message": "No user found",
                "data": [],
                "errors": [f"User {id} does not exist"]
            }), 404

        return jsonify({
            "status": "success",
            "message": f"User {id} found",
            "data": [user.to_safe_dict()],
            "errors": []
        }), 200

    except (DataError, ValueError) as err:
        return jsonify({
            "status": "error",
            "message": f"Invalid request while trying to get user {id}",
            "data": [],
            "errors": [str(err)]
        }), 400

    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred while trying to get user {id}",
            "data": [],
            "errors": [str(err)]
        }), 500

def get_confidential_user_info():
    try:
        user_id = g.user.get("userId")
        if not user_id:
            return jsonify({
                "status": "error",
                "message": "User ID not found in request context",
                "data": [],
                "errors": ["Missing authenticated user ID"]
            }), 400

        user = User.query.get(user_id)

        if not user:
            return jsonify({
                "status": "error",
                "message": "No user found",
                "data": [],
                "errors": [f"User {user_id} does not exist"]
            }), 404

        return jsonify({
            "status": "success",
            "message": f"User {user_id} found",
            "data": [user.to_safe_dict()],
            "errors": []
        }), 200

    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred while trying to get user {user_id}",
            "data": [],
            "errors": [str(err)]
        }), 500

def create_user():
    try:
        data = request.get_json()
        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        role = data.get("role", "").strip()

        errors = []

        if len(first_name) < 2:
            errors.append("First name must be at least 2 characters long")
        if len(last_name) < 2:
            errors.append("Last name must be at least 2 characters long")

        try:
            validate_email(email)
        except EmailNotValidError:
            errors.append("Email must be a valid email address")

        if len(username) < 6:
            errors.append("Username must be at least 6 characters long")

        # Password schema
        schema = PasswordValidator()
        schema.min(8).max(100).has().uppercase().has().lowercase().has().digits().has().symbols().has().no().spaces()
        if not schema.validate(password):
            failure_details = schema.validate(password, details=True)
            failures = "\n".join([f"{i+1}. {d['message'].replace('string', 'password')}" for i, d in enumerate(failure_details)])
            errors.append(f"Password validation failed:\n\n{failures}")

        if role not in ["tenant", "landlord"]:
            errors.append("Role must be one of the following: tenant, landlord")

        if errors:
            return jsonify({
                "status": "error",
                "message": "Unable to create user due to validation error(s)",
                "data": [],
                "errors": errors
            }), 400

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Begin transaction
        session = db.session
        try:
            user = User(
                firstName=first_name,
                lastName=last_name,
                username=username,
                email=email,
                password=hashed_pw,
                role=role
            )
            session.add(user)
            session.flush()  # Ensure user.id is populated

            token = jwt.encode(
                {
                    "id": user.id,
                    "exp": datetime.utcnow() + timedelta(hours=1)
                },
                os.getenv("JWT_SECRET"),
                algorithm="HS256"
            )

            host = os.getenv("HOST")
            port = os.getenv("FLASK_PORT")
            protocol = "http" if os.getenv("DEVELOPMENT") else "https"
            verification_link = f"{protocol}://{host}:{port}/api/users/verify?token={token}"

            try:
                send_email(
                to_email=email,
                subject="Homey - Email Verification",
                content=f"Hi {first_name},\n"
                    f"Thanks for registering! Please verify your email by clicking the link below:\n"
                    f"{verification_link}\n"
                    f"If you did not sign up for Homey, you can safely ignore this message."
            )
            except SMTPException as mail_err:
                session.rollback()
                return jsonify({
                    "status": "error",
                    "message": "Failed to send verification email",
                    "data": [],
                    "errors": [str(mail_err)]
                }), 500

            session.commit()
            return jsonify({
                "status": "success",
                "message": f"User {user.id} created",
                "data": [],
                "errors": []
            }), 201

        except SQLAlchemyError as err:
            session.rollback()
            return jsonify({
                "status": "error",
                "message": "An unexpected error occurred while trying to create user",
                "data": [],
                "errors": [str(err)]
            }), 500

    except Exception as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to create user",
            "data": [],
            "errors": [str(err)]
        }), 500

def login():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        errors = []
        if (not username and not email) or not password:
            if not username and not email:
                errors.append("Missing username or email")
            if not password:
                errors.append("Missing password")

            return jsonify({
                "status": "error",
                "message": "Missing fields in request",
                "data": [],
                "errors": errors
            }), 400

        user = None
        if username:
            user = User.query.filter_by(username=username).first()
        elif email:
            user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return jsonify({
                "status": "error",
                "message": "Invalid credentials",
                "data": [],
                "errors": ["Incorrect username/email or password"]
            }), 401

        if not user.verified:
            token = jwt.encode({ "id": user.id, "exp": datetime.utcnow() + timedelta(hours=1) }, os.getenv("JWT_SECRET"), algorithm="HS256")
            link = f"{'http' if os.getenv('DEVELOPMENT') else 'https'}://{os.getenv('HOST')}:{os.getenv('FLASK_PORT')}/api/users/verify?token={token}"
            
            send_email(
                to_email=user.email,
                subject="Homey - Email Verification",
                content=f"Hi {user.firstName},\n"
                    f"Thanks for registering! Please verify your email by clicking the link below:\n"
                    f"{link}\n"
                    f"If you did not sign up for Homey, you can safely ignore this message."
            )

            return jsonify({
                "status": "error",
                "message": f"Resent verification email to {user.email}",
                "data": [],
                "errors": ["Account is not verified"]
            }), 403

        token = jwt.encode(
            {
                "userId": user.id,
                "role": user.role.value,
                "verified": user.verified,
                "exp": datetime.utcnow() + timedelta(hours=1)
            },
            os.getenv("JWT_SECRET"),
            algorithm="HS256"
        )

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "data": [{ "token": token }],
            "errors": []
        }), 200

    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred during login",
            "data": [],
            "errors": [str(err)]
        }), 500

    except Exception as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred during login",
            "data": [],
            "errors": [str(err)]
        }), 500

def verify():
    try:
        token = request.args.get("token")
        decoded = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])

        user = User.query.get(decoded["id"])

        if not user:
            return jsonify({
                "status": "error",
                "message": "User not found",
                "data": [],
                "errors": [f"User {decoded['id']} not found for given token"]
            }), 404

        user.verified = True
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"User {decoded['id']} has been verified",
            "data": [],
            "errors": []
        }), 200

    except jwt.ExpiredSignatureError as err:
        return jsonify({
            "status": "error",
            "message": "The token has expired. Please login again to send another verification email",
            "data": [],
            "errors": [str(err)]
        }), 401

    except jwt.InvalidTokenError as err:
        return jsonify({
            "status": "error",
            "message": "Invalid token. Please log in or provide a valid token",
            "data": [],
            "errors": [str(err)]
        }), 401

    except jwt.exceptions.ImmatureSignatureError as err:
        return jsonify({
            "status": "error",
            "message": "The token is not yet active. Please check your system time",
            "data": [],
            "errors": [str(err)]
        }), 401

    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to verify the token",
            "data": [],
            "errors": [str(err)]
        }), 500

    except Exception as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to verify the token",
            "data": [],
            "errors": [str(err)]
        }), 500