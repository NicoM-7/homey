from flask import Blueprint
from controllers.conversation_controller import (
    get_conversations,
    get_conversation_by_id,
    create_dm,
    create_group_chat,
    add_participant,
    remove_participant
)
from middleware.authenticate_user import authenticate_user

conversation_routes = Blueprint("conversation_routes", __name__)

# GET /api/conversations/<groupId>
conversation_routes.route("/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_conversations))

# GET /api/conversations/<conversationId>
conversation_routes.route("/<int:conversation_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_conversation_by_id))

# POST /api/conversations/dm
conversation_routes.route("/dm", methods=["POST"])(authenticate_user(["tenant", "landlord"])(create_dm))

# POST /api/conversations/group
conversation_routes.route("/group", methods=["POST"])(authenticate_user(["tenant", "landlord"])(create_group_chat))

# POST /api/conversations/participants/add
conversation_routes.route("/participants/add", methods=["POST"])(authenticate_user(["tenant", "landlord"])(add_participant))

# DELETE /api/conversations/participants/remove
conversation_routes.route("/participants/remove", methods=["DELETE"])(authenticate_user(["tenant", "landlord"])(remove_participant)) 