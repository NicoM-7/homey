from flask import Blueprint
from controllers.user_controller import (
    get_users,
    get_user_by_id,
    get_confidential_user_info,
    create_user,
    login,
    verify
)
from middleware.authenticate_user import authenticate_user

user_routes = Blueprint("user_routes", __name__)

# GET /api/users
user_routes.route("/", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_users))

# GET /api/users/user/<id>
user_routes.route("/user/<int:id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_user_by_id))

# GET /api/users/me
user_routes.route("/me", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_confidential_user_info))

# GET /api/users/verify
user_routes.route("/verify", methods=["GET"])(verify)

# POST /api/users
user_routes.route("/", methods=["POST"])(create_user)

# POST /api/users/login
user_routes.route("/login", methods=["POST"])(login)
