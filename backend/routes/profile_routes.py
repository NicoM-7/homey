from flask import Blueprint
from controllers.profile_controller import (
    get_profile,
    update_profile
)
from middleware.authenticate_user import authenticate_user

profile_routes = Blueprint("profile_routes", __name__)

# GET /api/profile/<groupId>
profile_routes.route("/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_profile))

# POST /api/profile/updateProfile/<groupId>
profile_routes.route("/updateProfile/<int:group_id>", methods=["POST"])(authenticate_user(["tenant", "landlord"])(update_profile)) 