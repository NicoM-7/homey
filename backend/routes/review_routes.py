from flask import Blueprint
from controllers.review_controller import (
    get_reviews,
    create_review
)
from middleware.authenticate_user import authenticate_user

review_routes = Blueprint("review_routes", __name__)

# GET /api/reviews/<propertyId>
review_routes.route("/", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_reviews))

# POST /api/reviews
review_routes.route("/", methods=["POST"])(authenticate_user(["tenant"])(create_review)) 