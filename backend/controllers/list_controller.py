from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from models import List, Item
from db import db


def get_lists(group_id):
    """Get all lists for a group, optionally filtered by user"""
    try:
        user_id = request.args.get("userId")
        
        # Build the filter conditions
        filters = {"group_id": group_id}
        if user_id:
            filters["user_id"] = user_id
        
        # Fetch lists based on filters
        lists = List.query.filter_by(**filters).order_by(List.created_at.asc()).all()
        
        # If no lists found, return a 404 response
        if not lists:
            message = "No lists exist for the given user" if user_id else "No lists exist for this group"
            return jsonify({
                "status": "error",
                "message": message,
                "data": [],
                "errors": [f"No lists found with the provided criteria"]
            }), 404
        
        result = [list_item.to_dict() for list_item in lists]
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} list(s) found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to get the lists",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_list():
    """Create a new list"""
    try:
        data = request.get_json()
        user_id = data.get("userId")
        list_name = data.get("listName")
        group_id = data.get("groupId")
        
        user_list = List(
            group_id=group_id,
            user_id=user_id,
            list_name=list_name
        )
        
        db.session.add(user_list)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "List created",
            "data": user_list.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to create the list",
            "data": [],
            "errors": [str(err)]
        }), 500


def delete_list():
    """Delete a list and all its items"""
    try:
        data = request.get_json()
        list_id = data.get("listId")
        
        # Find and delete the list
        user_list = List.query.filter_by(list_id=list_id).first()
        
        if user_list:
            # Delete all items associated with this list
            Item.query.filter_by(list_id=list_id).delete()
            # Delete the list
            db.session.delete(user_list)
            db.session.commit()
            
            return jsonify({
                "status": "success",
                "message": "List deleted",
                "data": {"deleted": True},
                "errors": []
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "List not found",
                "data": [],
                "errors": [f"No list found with ID {list_id}"]
            }), 404
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to delete the list",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_items():
    """Get all items based on query parameters"""
    try:
        filters = dict(request.args)
        
        list_items = Item.query.filter_by(**filters).order_by(Item.created_at).all()
        
        if not list_items:
            return jsonify({
                "status": "error",
                "message": "No items exist for the users given list",
                "data": [],
                "errors": [f"No items found with data {filters}"]
            }), 404
        
        result = [item.to_dict() for item in list_items]
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} items found for the list",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to get the items",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_item():
    """Add an item to a list"""
    try:
        data = request.get_json()
        list_id = data.get("listId")
        item_name = data.get("item")
        assigned_to = data.get("assignedTo")
        
        # Check if the item already exists in the list
        existing_item = Item.query.filter_by(list_id=list_id, item=item_name).first()
        
        if existing_item:
            return jsonify({
                "status": "error",
                "message": "The item already exists in the list",
                "data": [],
                "errors": ["The item already exists in the list"]
            }), 400
        
        # Create the new item
        list_item = Item(
            list_id=list_id,
            item=item_name,
            assigned_to=assigned_to,
            purchased=False
        )
        
        db.session.add(list_item)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Item added to list",
            "data": list_item.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to create the item",
            "data": [],
            "errors": [str(err)]
        }), 500


def update_item():
    """Update an item in a list"""
    try:
        data = request.get_json()
        item_id = data.get("itemId")
        
        item = Item.query.get(item_id)
        
        if not item:
            return jsonify({
                "status": "error",
                "message": "Item not found",
                "data": [],
                "errors": [f"No item found with ID {item_id}"]
            }), 404
        
        # Update item fields
        for field, value in data.items():
            if field != "itemId" and hasattr(item, field):
                setattr(item, field, value)
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Item updated",
            "data": item.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to update the item",
            "data": [],
            "errors": [str(err)]
        }), 500


def delete_item():
    """Delete an item from a list"""
    try:
        data = request.get_json()
        item_id = data.get("itemId")
        
        item = Item.query.get(item_id)
        
        if not item:
            return jsonify({
                "status": "error",
                "message": "Item not found",
                "data": [],
                "errors": [f"No item found with ID {item_id}"]
            }), 404
        
        db.session.delete(item)
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
            "message": "An unexpected error occurred while trying to delete the item",
            "data": [],
            "errors": [str(err)]
        }), 500 