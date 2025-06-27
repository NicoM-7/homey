from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
import base64
from models import PropertyImage, Property
from db import db


def upload_property_image(id):
    """Upload a new image for a property"""
    try:
        data = request.get_json()
        label = data.get("label")
        image = data.get("image")
        description = data.get("description")
        property_id = id
        
        if not label or not image:
            return jsonify({
                "status": "error",
                "message": "Label and image are required",
                "data": None,
                "errors": ["Missing required fields"]
            }), 400
        
        # Ensure property exists
        property_item = Property.query.get(property_id)
        if not property_item:
            return jsonify({
                "status": "error",
                "message": "Property not found",
                "data": None,
                "errors": [f"No property found with ID {property_id}"]
            }), 404
        
        # Convert base64 image to binary
        try:
            image_binary = base64.b64decode(image)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Invalid image format",
                "data": None,
                "errors": ["Image must be valid base64"]
            }), 400
        
        # Create the new image
        new_image = PropertyImage(
            property_id=property_id,
            label=label,
            image=image_binary,
            description=description
        )
        
        db.session.add(new_image)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Image uploaded successfully",
            "data": new_image.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to upload image",
            "data": None,
            "errors": [str(err)]
        }), 500


def get_property_images(id):
    """Get all images for a property"""
    try:
        property_id = id
        images = PropertyImage.query.filter_by(property_id=property_id).all()
        
        if not images:
            return jsonify({
                "status": "error",
                "message": "No images found for this property",
                "data": [],
                "errors": [f"No images found for property ID {property_id}"]
            }), 404
        
        # Convert images to base64
        formatted_images = []
        for img in images:
            img_dict = img.to_dict()
            if img_dict.get("image"):
                img_dict["image"] = f"data:image/jpeg;base64,{base64.b64encode(img_dict['image']).decode('utf-8')}"
            else:
                img_dict["image"] = None
            formatted_images.append(img_dict)
        
        return jsonify({
            "status": "success",
            "message": f"{len(formatted_images)} image(s) found",
            "data": formatted_images,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve images",
            "data": None,
            "errors": [str(err)]
        }), 500


def update_property_image(id, image_id):
    """Update a property image"""
    try:
        data = request.get_json()
        label = data.get("label")
        image = data.get("image")
        description = data.get("description")
        
        property_image = PropertyImage.query.get(image_id)
        if not property_image:
            return jsonify({
                "status": "error",
                "message": "Image not found",
                "data": None,
                "errors": [f"No image found with ID {image_id}"]
            }), 404
        
        # Update fields
        if label:
            property_image.label = label
        if description:
            property_image.description = description
        if image:
            try:
                property_image.image = base64.b64decode(image)
            except Exception:
                return jsonify({
                    "status": "error",
                    "message": "Invalid image format",
                    "data": None,
                    "errors": ["Image must be valid base64"]
                }), 400
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Image updated successfully",
            "data": property_image.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to update image",
            "data": None,
            "errors": [str(err)]
        }), 500


def delete_property_image(id, image_id):
    """Delete a property image"""
    try:
        property_image = PropertyImage.query.get(image_id)
        if not property_image:
            return jsonify({
                "status": "error",
                "message": "Image not found",
                "data": None,
                "errors": [f"No image found with ID {image_id}"]
            }), 404
        
        db.session.delete(property_image)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Image deleted successfully",
            "data": None,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to delete image",
            "data": None,
            "errors": [str(err)]
        }), 500 