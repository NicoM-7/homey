from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from models import Chore, User
from db import db


def get_chores(group_id):
    """Get all chores for a group with optional assignee filter"""
    try:
        if not group_id:
            return jsonify({
                "status": "error",
                "message": "groupId is required",
                "data": [],
                "errors": ["groupId must be provided as a route parameter"]
            }), 400
        
        # Build the filter condition
        filters = {"group_id": group_id}
        
        assigned_to = request.args.get("assignedTo")
        if assigned_to:
            filters["assigned_to"] = assigned_to
        
        # Get all chores matching the filter
        chores = Chore.query.filter_by(**filters).order_by(Chore.created_at.desc()).all()
        
        if not chores:
            return jsonify({
                "status": "success",
                "message": "No chores found for this group",
                "data": [],
                "errors": []
            }), 200
        
        # Format chores with assignee information
        result = []
        for chore in chores:
            chore_dict = chore.to_dict()
            if chore.assigned_to:
                assignee = User.query.get(chore.assigned_to)
                if assignee:
                    chore_dict["assignee"] = {
                        "id": assignee.id,
                        "firstName": assignee.first_name,
                        "lastName": assignee.last_name,
                        "email": assignee.email
                    }
            result.append(chore_dict)
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} chore(s) found for group {group_id}",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while fetching chores",
            "data": [],
            "errors": [str(err)]
        }), 500


def add_chore():
    """Add a new chore"""
    try:
        data = request.get_json()
        chore_name = data.get("choreName")
        room = data.get("room")
        assigned_to = data.get("assignedTo")
        banner_image = data.get("bannerImage")
        due_date = data.get("dueDate")
        group_id = data.get("groupId")
        
        # Validate required fields
        if not chore_name or chore_name.strip() == "":
            return jsonify({
                "status": "error",
                "message": "Chore name is required",
                "data": [],
                "errors": ["Chore name cannot be empty"]
            }), 400
        
        if not room or room.strip() == "":
            return jsonify({
                "status": "error",
                "message": "Room is required",
                "data": [],
                "errors": ["Room cannot be empty"]
            }), 400
        
        # Create the chore
        chore = Chore(
            chore_name=chore_name,
            room=room,
            group_id=group_id,
            assigned_to=assigned_to,
            banner_image=banner_image,
            due_date=due_date,
            completed=False
        )
        
        db.session.add(chore)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Chore added successfully",
            "data": chore.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while adding the chore",
            "data": [],
            "errors": [str(err)]
        }), 500


def update_chore(id):
    """Update an existing chore"""
    try:
        data = request.get_json()
        chore_name = data.get("choreName")
        room = data.get("room")
        assigned_to = data.get("assignedTo")
        completed = data.get("completed")
        banner_image = data.get("bannerImage")
        due_date = data.get("dueDate")
        
        # Find the chore
        chore = Chore.query.get(id)
        
        if not chore:
            return jsonify({
                "status": "error",
                "message": "Chore not found",
                "data": [],
                "errors": [f"No chore found with ID: {id}"]
            }), 404
        
        # Update the chore fields
        if chore_name is not None:
            chore.chore_name = chore_name
        if room is not None:
            chore.room = room
        if assigned_to is not None:
            chore.assigned_to = assigned_to
        if completed is not None:
            chore.completed = completed
        if banner_image is not None:
            chore.banner_image = banner_image
        if due_date is not None:
            chore.due_date = due_date
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Chore updated successfully",
            "data": chore.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while updating the chore",
            "data": [],
            "errors": [str(err)]
        }), 500


def delete_chore(id):
    """Delete a chore"""
    try:
        # Find the chore
        chore = Chore.query.get(id)
        
        if not chore:
            return jsonify({
                "status": "error",
                "message": "Chore not found",
                "data": [],
                "errors": [f"No chore found with ID: {id}"]
            }), 404
        
        # Delete the chore
        db.session.delete(chore)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Chore deleted successfully",
            "data": [],
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while deleting the chore",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_chore_by_id(id):
    """Get a specific chore by ID"""
    try:
        chore = Chore.query.get(id)
        
        if not chore:
            return jsonify({
                "status": "error",
                "message": "Chore not found",
                "data": [],
                "errors": [f"No chore found with ID: {id}"]
            }), 404
        
        # Format chore with assignee information
        chore_dict = chore.to_dict()
        if chore.assigned_to:
            assignee = User.query.get(chore.assigned_to)
            if assignee:
                chore_dict["assignee"] = {
                    "id": assignee.id,
                    "firstName": assignee.first_name,
                    "lastName": assignee.last_name,
                    "email": assignee.email
                }
        
        return jsonify({
            "status": "success",
            "message": "Chore found",
            "data": chore_dict,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while fetching the chore",
            "data": [],
            "errors": [str(err)]
        }), 500 