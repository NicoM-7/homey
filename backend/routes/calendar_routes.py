from flask import Blueprint
from controllers.calendar_controller import (
    get_events,
    create_event,
    update_event,
    delete_event,
    get_upcoming_events
)
from middleware.authenticate_user import authenticate_user

calendar_routes = Blueprint("calendar_routes", __name__)

# GET /api/calendar/<groupId>
calendar_routes.route("/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_events))

# GET /api/calendar/upcoming/<groupId>
calendar_routes.route("/upcoming/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_upcoming_events))

# POST /api/calendar
calendar_routes.route("/", methods=["POST"])(authenticate_user(["tenant", "landlord"])(create_event))

# PUT /api/calendar/<id>
calendar_routes.route("/<int:id>", methods=["PUT"])(authenticate_user(["tenant", "landlord"])(update_event))

# DELETE /api/calendar/<id>
calendar_routes.route("/<int:id>", methods=["DELETE"])(authenticate_user(["tenant", "landlord"])(delete_event)) 