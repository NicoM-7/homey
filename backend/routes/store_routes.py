from flask import Blueprint
from controllers.store_controller import (
    get_store_entries,
    create_store_entry
)
from middleware.authenticate_user import authenticate_user

store_routes = Blueprint("store_routes", __name__)

# GET /api/stores/getEntries
store_routes.route("/getEntries", methods=["GET"])(get_store_entries)

# POST /api/stores/createEntries
store_routes.route("/createEntries", methods=["POST"])(create_store_entry) 