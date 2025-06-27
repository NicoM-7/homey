from flask import Blueprint
from controllers.list_controller import (
    get_lists,
    create_list,
    delete_list,
    get_items,
    create_item,
    update_item,
    delete_item
)
from middleware.authenticate_user import authenticate_user

list_routes = Blueprint("list_routes", __name__)

# GET /api/lists/items
list_routes.route("/items", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_items))

# GET /api/lists/<groupId>
list_routes.route("/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_lists))

# POST /api/lists/createList
list_routes.route("/createList", methods=["POST"])(authenticate_user(["tenant", "landlord"])(create_list))

# POST /api/lists/deleteList
list_routes.route("/deleteList", methods=["POST"])(authenticate_user(["tenant", "landlord"])(delete_list))

# POST /api/lists/createItem
list_routes.route("/createItem", methods=["POST"])(authenticate_user(["tenant", "landlord"])(create_item))

# POST /api/lists/updateItem
list_routes.route("/updateItem", methods=["POST"])(authenticate_user(["tenant", "landlord"])(update_item))

# POST /api/lists/deleteItem
list_routes.route("/deleteItem", methods=["POST"])(authenticate_user(["tenant", "landlord"])(delete_item)) 