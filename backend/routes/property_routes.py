from flask import Blueprint
from controllers.property_controller import (
    get_properties,
    get_property_by_id,
    get_properties_for_tenants,
    create_property,
    update_property,
    delete_property
)
from controllers.property_image_controller import (
    upload_property_image,
    update_property_image,
    delete_property_image,
    get_property_images
)
from middleware.authenticate_user import authenticate_user

property_routes = Blueprint("property_routes", __name__)

# GET /api/properties
property_routes.route("/", methods=["GET"])(authenticate_user(["landlord"])(get_properties))

# GET /api/properties/search
property_routes.route("/search", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_properties_for_tenants))

# GET /api/properties/<id>
property_routes.route("/<int:id>", methods=["GET"])(authenticate_user(["landlord"])(get_property_by_id))

# POST /api/properties
property_routes.route("/", methods=["POST"])(authenticate_user(["landlord"])(create_property))

# PUT /api/properties/<id>
property_routes.route("/<int:id>", methods=["PUT"])(authenticate_user(["landlord"])(update_property))

# DELETE /api/properties/<id>
property_routes.route("/<int:id>", methods=["DELETE"])(authenticate_user(["landlord"])(delete_property))

# GET /api/properties/<id>/images
property_routes.route("/<int:id>/images", methods=["GET"])(authenticate_user(["tenant", "landlord"])(get_property_images))

# POST /api/properties/<id>/images
property_routes.route("/<int:id>/images", methods=["POST"])(authenticate_user(["landlord"])(upload_property_image))

# PUT /api/properties/<id>/images/<imageId>
property_routes.route("/<int:id>/images/<int:image_id>", methods=["PUT"])(authenticate_user(["landlord"])(update_property_image))

# DELETE /api/properties/<id>/images/<imageId>
property_routes.route("/<int:id>/images/<int:image_id>", methods=["DELETE"])(authenticate_user(["landlord"])(delete_property_image)) 