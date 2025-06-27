from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
import base64
from models import Group, GroupParticipant, Property, User, Conversation, Participant, Profile
from db import db


def get_landlord_groups():
    """Get all groups where the authenticated user is the landlord"""
    try:
        user_id = g.user.get("userId")
        
        # Get groups where user is the landlord
        groups = Group.query.filter_by(landlord_id=user_id).all()
        
        formatted_groups = []
        for group in groups:
            group_dict = group.to_dict()
            
            # Get participants
            participants = []
            group_participants = GroupParticipant.query.filter_by(group_id=group.id).all()
            for gp in group_participants:
                user = User.query.get(gp.user_id)
                if user:
                    participants.append({
                        "id": user.id,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "email": user.email
                    })
            
            # Get property information
            property_info = None
            if group.property_id:
                property_item = Property.query.get(group.property_id)
                if property_item:
                    property_dict = property_item.to_dict()
                    exterior_image_base64 = None
                    if property_dict.get("exterior_image"):
                        exterior_image_base64 = f"data:image/jpeg;base64,{base64.b64encode(property_dict['exterior_image']).decode('utf-8')}"
                    
                    property_info = {
                        "id": property_dict["id"],
                        "name": property_dict["name"],
                        "exteriorImage": exterior_image_base64,
                        "address": property_dict["address"],
                        "city": property_dict["city"]
                    }
            
            formatted_group = {
                "id": group_dict["id"],
                "name": group_dict["name"],
                "property": property_info,
                "participants": participants
            }
            
            formatted_groups.append(formatted_group)
        
        return jsonify({
            "status": "success",
            "message": f"{len(formatted_groups)} group(s) found",
            "data": formatted_groups,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve groups",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_landlord_group_by_id(group_id):
    """Get a specific group by ID for the landlord"""
    try:
        user_id = g.user.get("userId")
        
        # Fetch the group where the landlord is the owner
        group = Group.query.filter_by(id=group_id, landlord_id=user_id).first()
        
        if not group:
            return jsonify({
                "status": "error",
                "message": "Group not found or does not belong to you",
                "data": None,
                "errors": ["No group found for the provided ID"]
            }), 404
        
        group_dict = group.to_dict()
        
        # Get participants
        participants = []
        group_participants = GroupParticipant.query.filter_by(group_id=group.id).all()
        for gp in group_participants:
            user = User.query.get(gp.user_id)
            if user:
                participants.append({
                    "id": user.id,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "email": user.email,
                    "username": user.username
                })
        
        # Get property information
        property_info = None
        if group.property_id:
            property_item = Property.query.get(group.property_id)
            if property_item:
                property_dict = property_item.to_dict()
                exterior_image_base64 = None
                if property_dict.get("exterior_image"):
                    exterior_image_base64 = f"data:image/jpeg;base64,{base64.b64encode(property_dict['exterior_image']).decode('utf-8')}"
                
                property_info = {
                    "id": property_dict["id"],
                    "name": property_dict["name"],
                    "exteriorImage": exterior_image_base64,
                    "address": property_dict["address"],
                    "city": property_dict["city"]
                }
        
        formatted_group = {
            "id": group_dict["id"],
            "name": group_dict["name"],
            "property": property_info,
            "participants": participants
        }
        
        return jsonify({
            "status": "success",
            "message": "Group retrieved successfully",
            "data": formatted_group,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve group",
            "data": None,
            "errors": [str(err)]
        }), 500


def get_tenant_groups():
    """Get all groups where the authenticated user is a participant"""
    try:
        user_id = g.user.get("userId")
        
        # Get groups where user is a participant
        group_participants = GroupParticipant.query.filter_by(tenant_id=user_id).all()
        
        formatted_groups = []
        for gp in group_participants:
            group = Group.query.get(gp.group_id)
            if not group:
                continue
            
            group_dict = group.to_dict()
            
            # Get landlord information
            landlord = User.query.get(group.landlord_id)
            landlord_info = None
            if landlord:
                landlord_info = {
                    "id": landlord.id,
                    "firstName": landlord.first_name,
                    "lastName": landlord.last_name,
                    "email": landlord.email
                }
            
            # Get property information
            property_info = None
            if group.property_id:
                property_item = Property.query.get(group.property_id)
                if property_item:
                    property_dict = property_item.to_dict()
                    exterior_image_base64 = None
                    if property_dict.get("exterior_image"):
                        exterior_image_base64 = f"data:image/jpeg;base64,{base64.b64encode(property_dict['exterior_image']).decode('utf-8')}"
                    
                    property_info = {
                        "id": property_dict["id"],
                        "name": property_dict["name"],
                        "exteriorImage": exterior_image_base64,
                        "address": property_dict["address"],
                        "city": property_dict["city"]
                    }
            
            formatted_group = {
                "id": group_dict["id"],
                "name": group_dict["name"],
                "property": property_info,
                "landlord": landlord_info
            }
            
            formatted_groups.append(formatted_group)
        
        return jsonify({
            "status": "success",
            "message": f"{len(formatted_groups)} group(s) found",
            "data": formatted_groups,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve groups",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_group():
    """Create a new group"""
    try:
        data = request.get_json()
        user_id = g.user.get("userId")
        
        name = data.get("name")
        property_id = data.get("propertyId")
        tenant_ids = data.get("tenantIds", [])
        
        if not name or not property_id or not tenant_ids or len(tenant_ids) < 1:
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "data": [],
                "errors": ["Name, propertyId, and at least one tenantId are required"]
            }), 400
        
        # Verify property exists and belongs to the landlord
        property_item = Property.query.filter_by(id=property_id, landlord_id=user_id).first()
        if not property_item:
            return jsonify({
                "status": "error",
                "message": "Property not found or does not belong to you",
                "data": [],
                "errors": [f"No property found with ID {property_id}"]
            }), 404
        
        # Verify all tenant IDs exist
        for tenant_id in tenant_ids:
            tenant = User.query.get(tenant_id)
            if not tenant:
                return jsonify({
                    "status": "error",
                    "message": f"Tenant with ID {tenant_id} not found",
                    "data": [],
                    "errors": [f"User {tenant_id} does not exist"]
                }), 404
        
        # Create the group
        new_group = Group(
            name=name,
            landlord_id=user_id,
            property_id=property_id
        )
        
        db.session.add(new_group)
        db.session.flush()  # Get the group ID
        
        # Add participants
        for tenant_id in tenant_ids:
            participant = GroupParticipant(
                group_id=new_group.id,
                user_id=tenant_id
            )
            db.session.add(participant)
        
        # Create a group conversation
        conversation = Conversation(
            name=f"{name} - Group Chat",
            conversation_type="group",
            group_id=new_group.id
        )
        db.session.add(conversation)
        db.session.flush()
        
        # Add all group members to the conversation
        # Add landlord
        landlord_participant = Participant(
            conversation_id=conversation.id,
            user_id=user_id
        )
        db.session.add(landlord_participant)
        
        # Add tenants
        for tenant_id in tenant_ids:
            tenant_participant = Participant(
                conversation_id=conversation.id,
                user_id=tenant_id
            )
            db.session.add(tenant_participant)
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Group created successfully",
            "data": new_group.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to create group",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_landlord_info(group_id):
    """Get landlord information for a group"""
    try:
        user_id = g.user.get("userId")
        
        # Verify user has access to this group
        group = Group.query.get(group_id)
        if not group:
            return jsonify({
                "status": "error",
                "message": "Group not found",
                "data": [],
                "errors": [f"No group found with ID {group_id}"]
            }), 404
        
        # Check if user is landlord or participant
        is_landlord = group.landlord_id == user_id
        is_participant = GroupParticipant.query.filter_by(group_id=group_id, user_id=user_id).first() is not None
        
        if not is_landlord and not is_participant:
            return jsonify({
                "status": "error",
                "message": "Access denied",
                "data": [],
                "errors": ["You do not have access to this group"]
            }), 403
        
        # Get landlord information
        landlord = User.query.get(group.landlord_id)
        if not landlord:
            return jsonify({
                "status": "error",
                "message": "Landlord not found",
                "data": [],
                "errors": [f"Landlord with ID {group.landlord_id} not found"]
            }), 404
        
        landlord_info = {
            "id": landlord.id,
            "firstName": landlord.first_name,
            "lastName": landlord.last_name,
            "email": landlord.email,
            "username": landlord.username
        }
        
        return jsonify({
            "status": "success",
            "message": "Landlord information retrieved successfully",
            "data": landlord_info,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve landlord information",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_property_info(group_id):
    """Get property information for a group"""
    try:
        user_id = g.user.get("userId")
        
        # Verify user has access to this group
        group = Group.query.get(group_id)
        if not group:
            return jsonify({
                "status": "error",
                "message": "Group not found",
                "data": [],
                "errors": [f"No group found with ID {group_id}"]
            }), 404
        
        # Check if user is landlord or participant
        is_landlord = group.landlord_id == user_id
        is_participant = GroupParticipant.query.filter_by(group_id=group_id, user_id=user_id).first() is not None
        
        if not is_landlord and not is_participant:
            return jsonify({
                "status": "error",
                "message": "Access denied",
                "data": [],
                "errors": ["You do not have access to this group"]
            }), 403
        
        # Get property information
        if not group.property_id:
            return jsonify({
                "status": "error",
                "message": "No property associated with this group",
                "data": [],
                "errors": ["This group has no associated property"]
            }), 404
        
        property_item = Property.query.get(group.property_id)
        if not property_item:
            return jsonify({
                "status": "error",
                "message": "Property not found",
                "data": [],
                "errors": [f"Property with ID {group.property_id} not found"]
            }), 404
        
        property_dict = property_item.to_dict()
        exterior_image_base64 = None
        if property_dict.get("exterior_image"):
            exterior_image_base64 = f"data:image/jpeg;base64,{base64.b64encode(property_dict['exterior_image']).decode('utf-8')}"
        
        property_info = {
            "id": property_dict["id"],
            "name": property_dict["name"],
            "exteriorImage": exterior_image_base64,
            "address": property_dict["address"],
            "city": property_dict["city"],
            "propertyDescription": property_dict.get("property_description"),
            "bedrooms": property_dict["bedrooms"],
            "price": property_dict["price"]
        }
        
        return jsonify({
            "status": "success",
            "message": "Property information retrieved successfully",
            "data": property_info,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve property information",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_group_participants(group_id):
    """Get all participants of a group"""
    try:
        user_id = g.user.get("userId")
        
        # Verify user has access to this group
        group = Group.query.get(group_id)
        if not group:
            return jsonify({
                "status": "error",
                "message": "Group not found",
                "data": [],
                "errors": [f"No group found with ID {group_id}"]
            }), 404
        
        # Check if user is landlord or participant
        is_landlord = group.landlord_id == user_id
        is_participant = GroupParticipant.query.filter_by(group_id=group_id, user_id=user_id).first() is not None
        
        if not is_landlord and not is_participant:
            return jsonify({
                "status": "error",
                "message": "Access denied",
                "data": [],
                "errors": ["You do not have access to this group"]
            }), 403
        
        # Get participants
        participants = []
        group_participants = GroupParticipant.query.filter_by(group_id=group_id).all()
        for gp in group_participants:
            user = User.query.get(gp.user_id)
            if user:
                participants.append({
                    "id": user.id,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "email": user.email,
                    "username": user.username
                })
        
        return jsonify({
            "status": "success",
            "message": f"{len(participants)} participant(s) found",
            "data": participants,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve group participants",
            "data": [],
            "errors": [str(err)]
        }), 500


def update_group(group_id):
    """Update a group"""
    try:
        data = request.get_json()
        user_id = g.user.get("userId")
        
        # Only landlord can update the group
        group = Group.query.filter_by(id=group_id, landlord_id=user_id).first()
        if not group:
            return jsonify({
                "status": "error",
                "message": "Group not found or you don't have permission to update it",
                "data": [],
                "errors": [f"No group found with ID {group_id} for landlord {user_id}"]
            }), 404
        
        # Update group fields
        if "name" in data:
            group.name = data["name"]
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Group updated successfully",
            "data": group.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to update group",
            "data": [],
            "errors": [str(err)]
        }), 500


def delete_group(group_id):
    """Delete a group"""
    try:
        user_id = g.user.get("userId")
        
        # Only landlord can delete the group
        group = Group.query.filter_by(id=group_id, landlord_id=user_id).first()
        if not group:
            return jsonify({
                "status": "error",
                "message": "Group not found or you don't have permission to delete it",
                "data": [],
                "errors": [f"No group found with ID {group_id} for landlord {user_id}"]
            }), 404
        
        # Delete associated records
        GroupParticipant.query.filter_by(group_id=group_id).delete()
        
        # Delete associated conversations and participants
        conversations = Conversation.query.filter_by(group_id=group_id).all()
        for conv in conversations:
            Participant.query.filter_by(conversation_id=conv.id).delete()
            db.session.delete(conv)
        
        # Delete the group
        db.session.delete(group)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Group deleted successfully",
            "data": [],
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to delete group",
            "data": [],
            "errors": [str(err)]
        }), 500 