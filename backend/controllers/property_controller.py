from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_
import base64
from models import Property, PropertyImage, User
from db import db
import logging

def get_properties():
    """Get all properties for the authenticated landlord"""
    try:
        user_id = g.user.get("userId")
        
        properties = Property.query.filter_by(landlord_id=user_id).all()
        
        if not properties:
            return jsonify({
                "status": "error",
                "message": "No properties found",
                "data": [],
                "errors": [f"No properties found for landlord {user_id}"]
            }), 404
        
        # Format properties with base64 image conversion
        formatted_properties = []
        for property_item in properties:
            property_dict = property_item.to_dict()
            
            # Convert exterior image to base64 if it exists
            if property_dict.get("exterior_image"):
                property_dict["exteriorImage"] = f"data:image/jpeg;base64,{base64.b64encode(property_dict['exterior_image']).decode('utf-8')}"
                property_dict.pop("exterior_image", None)  # Remove the raw binary data
            else:
                property_dict["exteriorImage"] = None
            
            # Get property images
            images = PropertyImage.query.filter_by(property_id=property_item.id).all()
            property_dict["images"] = [img.to_dict() for img in images]
            
            formatted_properties.append(property_dict)
        
        return jsonify({
            "status": "success",
            "message": f"{len(formatted_properties)} property(s) found",
            "data": formatted_properties,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve properties",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_property_by_id(id):
    """Get a specific property by ID for the authenticated landlord"""
    try:
        user_id = g.user.get("userId")
        
        property_item = Property.query.filter_by(id=id, landlord_id=user_id).first()
        
        if not property_item:
            return jsonify({
                "status": "error",
                "message": "Property not found",
                "data": None,
                "errors": [f"No property found with ID {id}"]
            }), 404
        
        # Format property with base64 image conversion
        property_dict = property_item.to_dict()
        
        # Convert exterior image to base64 if it exists
        if property_dict.get("exterior_image"):
            property_dict["exteriorImage"] = f"data:image/jpeg;base64,{base64.b64encode(property_dict['exterior_image']).decode('utf-8')}"
            property_dict.pop("exterior_image", None)
        else:
            property_dict["exteriorImage"] = None
        
        # Get property images
        images = PropertyImage.query.filter_by(property_id=property_item.id).all()
        property_dict["images"] = [img.to_dict() for img in images]
        
        return jsonify({
            "status": "success",
            "message": "Property retrieved successfully",
            "data": property_dict,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve property",
            "data": None,
            "errors": [str(err)]
        }), 500


def get_properties_for_tenants():
    """Get properties for tenant search with filters"""
    try:
        # Get query parameters
        max_price = request.args.get("maxPrice")
        city = request.args.get("city")
        property_type = request.args.get("propertyType")
        bedrooms = request.args.get("bedrooms")
        
        # Start with base filter - only available properties
        query = Property.query.filter_by(availability=True)
        
        # Apply filters if provided
        if max_price and max_price.isdigit():
            query = query.filter(Property.price <= int(max_price))
        
        if city and city.strip():
            query = query.filter(Property.city.ilike(f"%{city}%"))
        
        if property_type and property_type != "Any":
            query = query.filter(Property.property_type == property_type)
        
        if bedrooms and bedrooms.isdigit():
            query = query.filter(Property.bedrooms >= int(bedrooms))
        
        # Execute query and get landlord information
        properties = query.all()
        
        if not properties:
            return jsonify({
                "status": "error",
                "message": "No properties found matching your criteria",
                "data": [],
                "errors": ["No properties match the search filters"]
            }), 404
        
        # Format properties with landlord information
        formatted_properties = []
        for property_item in properties:
            property_dict = property_item.to_dict()
            
            # Get landlord information
            landlord = User.query.get(property_item.landlord_id)
            
            # Convert exterior image to base64 if it exists
            exterior_image_base64 = None
            if property_dict.get("exterior_image"):
                exterior_image_base64 = f"data:image/jpeg;base64,{base64.b64encode(property_dict['exterior_image']).decode('utf-8')}"
            
            formatted_property = {
                "id": property_dict["id"],
                "name": property_dict["name"],
                "address": property_dict["address"],
                "city": property_dict["city"],
                "price": property_dict["price"],
                "bedrooms": property_dict["bedrooms"],
                "propertyType": property_dict.get("property_type"),
                "availability": property_dict["availability"],
                "description": property_dict.get("property_description"),
                "exteriorImage": exterior_image_base64,
                "landlord": {
                    "id": landlord.id,
                    "name": f"{landlord.firstName[0]}. {landlord.lastName}",
                    "firstName": landlord.firstName,
                    "lastName": landlord.lastName,
                    "email": landlord.email
                } if landlord else None
            }
            
            formatted_properties.append(formatted_property)
        
        return jsonify({
            "status": "success",
            "message": f"{len(formatted_properties)} property(s) found",
            "data": formatted_properties,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve properties",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_property():
    """Create a new property"""
    try:
        data = request.get_json()
        user_id = g.user.get("userId")
        
        name = data.get("name")
        address = data.get("address")
        city = data.get("city")
        property_description = data.get("propertyDescription")
        bedrooms = data.get("bedrooms")
        price = data.get("price")
        property_type = data.get("propertyType")
        availability = data.get("availability", True)
        exterior_image = data.get("exteriorImage")
        images = data.get("images", [])
        
        # Validate required fields
        if not all([name, address, city, bedrooms, price, property_type]) or exterior_image is None:
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "data": [],
                "errors": ["Name, address, city, bedrooms, price, property type, and exterior image are required"]
            }), 400
        
        # Convert base64 image to binary if provided
        exterior_image_binary = None
        if exterior_image:
            try:
                exterior_image_binary = base64.b64decode(exterior_image)
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": "Invalid exterior image format",
                    "data": [],
                    "errors": ["Exterior image must be valid base64"]
                }), 400
        
        # Create the property
        new_property = Property(
            landlord_id=user_id,
            name=name,
            address=address,
            city=city,
            property_description=property_description,
            bedrooms=bedrooms,
            price=price,
            property_type=property_type,
            availability=availability,
            exterior_image=exterior_image_binary
        )
        
        db.session.add(new_property)
        db.session.flush()  # Get the property ID
        
        # Add property images if provided
        for img_data in images:
            if img_data.get("image") and img_data.get("label"):
                try:
                    image_binary = base64.b64decode(img_data["image"])
                    property_image = PropertyImage(
                        property_id=new_property.id,
                        label=img_data["label"],
                        image=image_binary,
                        description=img_data.get("description")
                    )
                    db.session.add(property_image)
                except Exception:
                    continue  # Skip invalid images
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Property created successfully",
            "data": new_property.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        logging.warning(f"Error creating property: {err}")
        return jsonify({
            "status": "error",
            "message": "Failed to create property",
            "data": [],
            "errors": [str(err)]
        }), 500


def update_property(id):
    """Update an existing property"""
    try:
        data = request.get_json()
        user_id = g.user.get("userId")
        
        property_item = Property.query.filter_by(id=id, landlord_id=user_id).first()
        
        if not property_item:
            return jsonify({
                "status": "error",
                "message": "Property not found",
                "data": [],
                "errors": [f"No property found with ID {id}"]
            }), 404
        
        # Update property fields
        for field, value in data.items():
            if field == "exteriorImage" and value:
                try:
                    property_item.exterior_image = base64.b64decode(value)
                except Exception:
                    continue  # Skip invalid image
            elif field == "propertyDescription":
                property_item.property_description = value
            elif field == "propertyType":
                property_item.property_type = value
            elif hasattr(property_item, field):
                setattr(property_item, field, value)
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Property updated successfully",
            "data": property_item.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to update property",
            "data": [],
            "errors": [str(err)]
        }), 500


def delete_property(id):
    """Delete a property"""
    try:
        user_id = g.user.get("userId")
        
        property_item = Property.query.filter_by(id=id, landlord_id=user_id).first()
        
        if not property_item:
            return jsonify({
                "status": "error",
                "message": "Property not found",
                "data": [],
                "errors": [f"No property found with ID {id}"]
            }), 404
        
        # Delete associated property images first
        PropertyImage.query.filter_by(property_id=id).delete()
        
        # Delete the property
        db.session.delete(property_item)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Property deleted successfully",
            "data": [],
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to delete property",
            "data": [],
            "errors": [str(err)]
        }), 500 