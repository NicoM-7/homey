from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from models import Inventory
from db import db


def get_inventory(group_id):
    """Get the inventory for a group"""
    try:
        # Get the inventory based on the group id
        inventory_list = Inventory.query.filter_by(group_id=group_id).order_by(Inventory.created_at).all()
        
        if not inventory_list:
            return jsonify({
                "status": "success",
                "message": "No inventory exists for the given house",
                "data": "empty",
                "errors": []
            }), 204
        
        result = [item.to_dict() for item in inventory_list]
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} inventory found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to get the inventory",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_low_item(group_id):
    """Get all items that have a quantity of 1 or less"""
    try:
        inventory_items = Inventory.query.filter_by(
            group_id=group_id,
            quantity=1
        ).order_by(Inventory.created_at).all()
        
        if not inventory_items:
            return jsonify({
                "status": "success",
                "message": "No low inventory items for the given house",
                "data": "empty",
                "errors": []
            }), 204
        
        result = [item.to_dict() for item in inventory_items]
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} low inventory items found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to get low inventory items",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_inventory():
    """Create a new inventory item or increment existing one"""
    try:
        data = request.get_json()
        item_name = data.get("itemName")
        group_id = data.get("groupId")
        
        if not item_name or not group_id:
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "data": [],
                "errors": ["itemName and groupId are required"]
            }), 400
        
        # Check if the item already exists in the inventory
        inventory_item = Inventory.query.filter_by(
            item_name=item_name.lower(),
            group_id=group_id
        ).first()
        
        # If item doesn't exist, create it
        if not inventory_item:
            new_inventory_item = Inventory(
                group_id=group_id,
                item_name=item_name.lower(),
                quantity=1
            )
            
            db.session.add(new_inventory_item)
            db.session.commit()
            
            return jsonify({
                "status": "success",
                "message": "Item added to inventory",
                "data": new_inventory_item.to_dict(),
                "errors": []
            }), 201
        
        # If item exists, increment its quantity
        else:
            inventory_item.quantity += 1
            db.session.commit()
            
            return jsonify({
                "status": "success",
                "message": "Item quantity updated in inventory",
                "data": inventory_item.to_dict(),
                "errors": []
            }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to create/update inventory",
            "data": [],
            "errors": [str(err)]
        }), 500


def delete_inventory_item():
    """Delete an inventory item"""
    try:
        data = request.get_json()
        item_id = data.get("itemId")
        
        if not item_id:
            return jsonify({
                "status": "error",
                "message": "Missing itemId",
                "data": [],
                "errors": ["itemId is required"]
            }), 400
        
        # Check if the item exists
        inventory_item = Inventory.query.filter_by(item_id=item_id).first()
        
        if not inventory_item:
            return jsonify({
                "status": "error",
                "message": "The inventory item does not exist",
                "data": [],
                "errors": ["No inventory item exists with the given ID"]
            }), 404
        
        # Delete the inventory item
        db.session.delete(inventory_item)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Item deleted",
            "data": {"deleted": True},
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to delete inventory item",
            "data": [],
            "errors": [str(err)]
        }), 500


def remove_quantity():
    """Remove quantity from an inventory item"""
    try:
        data = request.get_json()
        item_id = data.get("itemId")
        quantity = data.get("quantity", 1)
        
        if not item_id:
            return jsonify({
                "status": "error",
                "message": "Missing itemId",
                "data": [],
                "errors": ["itemId is required"]
            }), 400
        
        # Find the item
        inventory_item = Inventory.query.filter_by(item_id=item_id).first()
        
        if not inventory_item:
            return jsonify({
                "status": "error",
                "message": "Inventory item not found",
                "data": [],
                "errors": [f"No inventory item found with ID {item_id}"]
            }), 404
        
        # If the inventory item quantity is already zero, send an error
        if inventory_item.quantity == 0:
            return jsonify({
                "status": "error",
                "message": "Cannot remove quantity from an item with zero quantity",
                "data": [],
                "errors": ["Item quantity is already at zero"]
            }), 400
        
        # Remove quantity
        new_quantity = max(0, inventory_item.quantity - quantity)
        inventory_item.quantity = new_quantity
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": f"Quantity removed. New quantity: {new_quantity}",
            "data": inventory_item.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to remove quantity",
            "data": [],
            "errors": [str(err)]
        }), 500 