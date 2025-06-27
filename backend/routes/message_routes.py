from flask import Blueprint
from controllers.message_controller import (
    send_message,
    get_messages,
    mark_message_as_read
)
from middleware.authenticate_user import authenticate_user

message_routes = Blueprint("message_routes", __name__)

# POST /api/messages/send
message_routes.route("/send", methods=["POST"])(authenticate_user(["tenant", "landlord"])(send_message))

# GET /api/messages/conversation/<conversationId>
message_routes.route("/conversation/<int:conversation_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_messages))

# PATCH /api/messages/read
message_routes.route("/read", methods=["PATCH"])(authenticate_user(["tenant", "landlord"])(mark_message_as_read)) 