from flask import Blueprint
from controllers.inventory_controller import (
    get_inventory,
    get_low_item,
    create_inventory,
    delete_inventory_item,
    remove_quantity
)
from middleware.authenticate_user import authenticate_user

inventory_routes = Blueprint("inventory_routes", __name__)

# GET /api/inventory/<groupId>
inventory_routes.route("/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_inventory))

# GET /api/inventory/getLowItem/<groupId>
inventory_routes.route("/getLowItem/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_low_item))

# POST /api/inventory/createInventory
inventory_routes.route("/createInventory", methods=["POST"])(authenticate_user(["tenant", "landlord"])(create_inventory))

# POST /api/inventory/deleteItem
inventory_routes.route("/deleteItem", methods=["POST"])(authenticate_user(["tenant", "landlord"])(delete_inventory_item))

# POST /api/inventory/removeQuantity
inventory_routes.route("/removeQuantity", methods=["POST"])(authenticate_user(["tenant", "landlord"])(remove_quantity)) 