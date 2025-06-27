from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from models import Conversation, Participant, User, Group
from db import db


def get_conversations(group_id):
    """Get all conversations for a group"""
    try:
        user_id = g.user.get("userId")
        
        # Get conversations where the user is a participant
        conversations = Conversation.query.filter_by(group_id=group_id).all()
        
        result = []
        for conversation in conversations:
            # Check if user is a participant
            is_participant = Participant.query.filter_by(
                conversation_id=conversation.id,
                user_id=user_id
            ).first()
            
            if is_participant:
                result.append(conversation.to_dict())
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} conversations found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve conversations",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_conversation_by_id(conversation_id):
    """Get a specific conversation by ID"""
    try:
        user_id = g.user.get("userId")
        
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({
                "status": "error",
                "message": "Conversation not found",
                "data": [],
                "errors": [f"No conversation found with ID {conversation_id}"]
            }), 404
        
        # Check if user is a participant
        is_participant = Participant.query.filter_by(
            conversation_id=conversation_id,
            user_id=user_id
        ).first()
        
        if not is_participant:
            return jsonify({
                "status": "error",
                "message": "Access denied",
                "data": [],
                "errors": ["You are not a participant in this conversation"]
            }), 403
        
        return jsonify({
            "status": "success",
            "message": "Conversation retrieved successfully",
            "data": conversation.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve conversation",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_dm():
    """Create a direct message conversation"""
    try:
        data = request.get_json()
        user_id = data.get("userId")
        current_user_id = g.user.get("userId")
        
        if not user_id:
            return jsonify({
                "status": "error",
                "message": "Missing userId",
                "data": [],
                "errors": ["userId is required"]
            }), 400
        
        if user_id == current_user_id:
            return jsonify({
                "status": "error",
                "message": "Cannot create DM with yourself",
                "data": [],
                "errors": ["Cannot create a DM with yourself"]
            }), 400
        
        # Create conversation
        conversation = Conversation(
            conversation_type="dm",
            name=f"DM-{current_user_id}-{user_id}"
        )
        
        db.session.add(conversation)
        db.session.flush()  # Get conversation ID
        
        # Add participants
        participant1 = Participant(conversation_id=conversation.id, user_id=current_user_id)
        participant2 = Participant(conversation_id=conversation.id, user_id=user_id)
        
        db.session.add(participant1)
        db.session.add(participant2)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "DM conversation created",
            "data": conversation.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to create DM",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_group_chat():
    """Create a group chat conversation"""
    try:
        data = request.get_json()
        name = data.get("name")
        participant_ids = data.get("participantIds", [])
        current_user_id = g.user.get("userId")
        
        if not name:
            return jsonify({
                "status": "error",
                "message": "Missing conversation name",
                "data": [],
                "errors": ["name is required"]
            }), 400
        
        # Create conversation
        conversation = Conversation(
            conversation_type="group",
            name=name
        )
        
        db.session.add(conversation)
        db.session.flush()  # Get conversation ID
        
        # Add current user as participant
        current_participant = Participant(conversation_id=conversation.id, user_id=current_user_id)
        db.session.add(current_participant)
        
        # Add other participants
        for participant_id in participant_ids:
            if participant_id != current_user_id:
                participant = Participant(conversation_id=conversation.id, user_id=participant_id)
                db.session.add(participant)
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Group chat created",
            "data": conversation.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to create group chat",
            "data": [],
            "errors": [str(err)]
        }), 500


def add_participant():
    """Add a participant to a conversation"""
    try:
        data = request.get_json()
        conversation_id = data.get("conversationId")
        user_id = data.get("userId")
        
        if not conversation_id or not user_id:
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "data": [],
                "errors": ["conversationId and userId are required"]
            }), 400
        
        # Check if conversation exists
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({
                "status": "error",
                "message": "Conversation not found",
                "data": [],
                "errors": [f"No conversation found with ID {conversation_id}"]
            }), 404
        
        # Check if user is already a participant
        existing_participant = Participant.query.filter_by(
            conversation_id=conversation_id,
            user_id=user_id
        ).first()
        
        if existing_participant:
            return jsonify({
                "status": "error",
                "message": "User is already a participant",
                "data": [],
                "errors": ["User is already a participant in this conversation"]
            }), 400
        
        # Add participant
        participant = Participant(conversation_id=conversation_id, user_id=user_id)
        db.session.add(participant)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Participant added successfully",
            "data": participant.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to add participant",
            "data": [],
            "errors": [str(err)]
        }), 500


def remove_participant():
    """Remove a participant from a conversation"""
    try:
        data = request.get_json()
        conversation_id = data.get("conversationId")
        user_id = data.get("userId")
        
        if not conversation_id or not user_id:
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "data": [],
                "errors": ["conversationId and userId are required"]
            }), 400
        
        # Find and remove participant
        participant = Participant.query.filter_by(
            conversation_id=conversation_id,
            user_id=user_id
        ).first()
        
        if not participant:
            return jsonify({
                "status": "error",
                "message": "Participant not found",
                "data": [],
                "errors": ["User is not a participant in this conversation"]
            }), 404
        
        db.session.delete(participant)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Participant removed successfully",
            "data": [],
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to remove participant",
            "data": [],
            "errors": [str(err)]
        }), 500 