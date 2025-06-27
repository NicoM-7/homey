from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from models import Profile, User, Group
from db import db


def get_profile(group_id):
    """Get profile for a specific group"""
    try:
        user_id = g.user.get("userId")
        
        # Get the user's profile for the specific group
        profile = Profile.query.filter_by(user_id=user_id, group_id=group_id).first()
        
        if not profile:
            return jsonify({
                "status": "error",
                "message": "Profile not found",
                "data": [],
                "errors": [f"No profile found for user {user_id} in group {group_id}"]
            }), 404
        
        return jsonify({
            "status": "success",
            "message": "Profile retrieved successfully",
            "data": profile.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to get the profile",
            "data": [],
            "errors": [str(err)]
        }), 500


def update_profile(group_id):
    """Update profile for a specific group"""
    try:
        data = request.get_json()
        user_id = g.user.get("userId")
        
        # Get the user's profile for the specific group
        profile = Profile.query.filter_by(user_id=user_id, group_id=group_id).first()
        
        if not profile:
            # Create new profile if it doesn't exist
            profile = Profile(
                user_id=user_id,
                group_id=group_id
            )
            db.session.add(profile)
        
        # Update profile fields
        for field, value in data.items():
            if hasattr(profile, field):
                setattr(profile, field, value)
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Profile updated successfully",
            "data": profile.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to update the profile",
            "data": [],
            "errors": [str(err)]
        }), 500 