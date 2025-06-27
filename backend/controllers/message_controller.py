from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from models import Message, Conversation, User
from db import db


def send_message():
    """Send a message in a conversation"""
    try:
        data = request.get_json()
        conversation_id = data.get("conversationId")
        content = data.get("content")
        sender_id = g.user.get("userId")
        
        if not conversation_id or not content:
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "data": [],
                "errors": ["conversationId and content are required"]
            }), 400
        
        # Verify conversation exists
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({
                "status": "error",
                "message": "Conversation not found",
                "data": [],
                "errors": [f"No conversation found with ID {conversation_id}"]
            }), 404
        
        # Create the message
        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
            is_read=False
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Message sent successfully",
            "data": message.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to send message",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_messages(conversation_id):
    """Get all messages for a conversation"""
    try:
        # Verify conversation exists
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return jsonify({
                "status": "error",
                "message": "Conversation not found",
                "data": [],
                "errors": [f"No conversation found with ID {conversation_id}"]
            }), 404
        
        # Get messages with sender information
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
        
        result = []
        for message in messages:
            message_dict = message.to_dict()
            sender = User.query.get(message.sender_id)
            message_dict["sender"] = sender.to_safe_dict() if sender else None
            result.append(message_dict)
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} messages found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve messages",
            "data": [],
            "errors": [str(err)]
        }), 500


def mark_message_as_read():
    """Mark a message as read"""
    try:
        data = request.get_json()
        message_id = data.get("messageId")
        
        if not message_id:
            return jsonify({
                "status": "error",
                "message": "Missing messageId",
                "data": [],
                "errors": ["messageId is required"]
            }), 400
        
        message = Message.query.get(message_id)
        if not message:
            return jsonify({
                "status": "error",
                "message": "Message not found",
                "data": [],
                "errors": [f"No message found with ID {message_id}"]
            }), 404
        
        message.is_read = True
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Message marked as read",
            "data": message.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to mark message as read",
            "data": [],
            "errors": [str(err)]
        }), 500 