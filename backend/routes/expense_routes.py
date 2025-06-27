from flask import Blueprint
from controllers.expense_controller import (
    add_expense,
    get_expenses,
    complete_expense
)
from middleware.authenticate_user import authenticate_user

expense_routes = Blueprint("expense_routes", __name__)

# POST /api/expenses
expense_routes.route("/", methods=["POST"])(authenticate_user(["tenant", "landlord"])(add_expense))

# GET /api/expenses/<groupId>
expense_routes.route("/<int:group_id>", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_expenses))

# PUT /api/expenses/<id>/complete
expense_routes.route("/<int:id>/complete", methods=["PUT"])(authenticate_user(["tenant", "landlord"])(complete_expense)) 