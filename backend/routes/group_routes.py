from flask import Blueprint
from controllers.group_controller import (
    create_group,
    get_landlord_groups,
    get_landlord_group_by_id,
    get_tenant_groups,
    get_landlord_info,
    get_property_info,
    get_group_participants,
    delete_group,
    update_group,
)
from middleware.authenticate_user import authenticate_user

group_routes = Blueprint("group_routes", __name__)

# GET /api/groups/landlord
group_routes.route("/landlord", methods=["GET"])(authenticate_user(["landlord"])(get_landlord_groups))

# GET /api/groups/tenant
group_routes.route("/tenant", methods=["GET"])(authenticate_user(["tenant"])(get_tenant_groups))

# GET /api/groups/<groupId>/landlord
group_routes.route("/<int:group_id>/landlord", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_landlord_info))

# GET /api/groups/<groupId>/property
group_routes.route("/<int:group_id>/property", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_property_info))

# GET /api/groups/<groupId>
group_routes.route("/<int:group_id>", methods=["GET"])(authenticate_user(["landlord"])(get_landlord_group_by_id))

# GET /api/groups/<groupId>/participants
group_routes.route("/<int:group_id>/participants", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_group_participants))

# POST /api/groups
group_routes.route("/", methods=["POST"])(authenticate_user(["landlord"])(create_group))

# PUT /api/groups/<groupId>
group_routes.route("/<int:group_id>", methods=["PUT"])(authenticate_user(["landlord"])(update_group))

# DELETE /api/groups/<groupId>
group_routes.route("/<int:group_id>", methods=["DELETE"])(authenticate_user(["landlord"])(delete_group)) 