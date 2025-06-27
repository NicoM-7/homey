from flask import Blueprint
from controllers.chores_controller import (
    get_chores,
    add_chore,
    update_chore,
    delete_chore,
    get_chore_by_id
)
from middleware.authenticate_user import authenticate_user

chores_routes = Blueprint("chores_routes", __name__)

# GET /api/chores/<groupId>
chores_routes.route("/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_chores))

# GET /api/chores/<id>
chores_routes.route("/<int:id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_chore_by_id))

# POST /api/chores
chores_routes.route("/", methods=["POST"])(authenticate_user(["tenant", "landlord"])(add_chore))

# PUT /api/chores/<id>
chores_routes.route("/<int:id>", methods=["PUT"])(authenticate_user(["tenant", "landlord"])(update_chore))

# DELETE /api/chores/<id>
chores_routes.route("/<int:id>", methods=["DELETE"])(authenticate_user(["tenant", "landlord"])(delete_chore)) 