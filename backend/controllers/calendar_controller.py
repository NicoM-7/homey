from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from models import CalendarEvent, User
from db import db


def get_events(group_id):
    """Get all events for a group"""
    try:
        if not group_id:
            return jsonify({
                "status": "error",
                "message": "groupId is required",
                "data": [],
                "errors": ["groupId must be provided in the request parameters"]
            }), 400
        
        # Get events with user information
        events = CalendarEvent.query.filter_by(group_id=group_id).all()
        
        if not events:
            return jsonify({
                "status": "error",
                "message": "No calendar events found",
                "data": [],
                "errors": ["No events found in the calendar"]
            }), 404
        
        # Format events with user data
        result = []
        for event in events:
            event_dict = event.to_dict()
            user = User.query.get(event.user_id)
            if user:
                event_dict["user"] = {
                    "id": user.id,
                    "firstName": user.first_name,
                    "lastName": user.last_name
                }
            result.append(event_dict)
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} event(s) found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while fetching events",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_upcoming_events(group_id):
    """Get events within 48 hours"""
    try:
        if not group_id:
            return jsonify({
                "status": "error",
                "message": "groupId is required",
                "data": [],
                "errors": ["groupId must be provided in the request parameters"]
            }), 400
        
        # Calculate date range (next 48 hours)
        now = datetime.now()
        future_date = now + timedelta(hours=48)
        
        # Get upcoming events
        events = CalendarEvent.query.filter(
            CalendarEvent.group_id == group_id,
            CalendarEvent.event_date >= now.date(),
            CalendarEvent.event_date <= future_date.date()
        ).all()
        
        # Format events with user data
        result = []
        for event in events:
            event_dict = event.to_dict()
            user = User.query.get(event.user_id)
            if user:
                event_dict["user"] = {
                    "id": user.id,
                    "firstName": user.first_name,
                    "lastName": user.last_name
                }
            result.append(event_dict)
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} upcoming event(s) found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while fetching upcoming events",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_event():
    """Create a new calendar event"""
    try:
        data = request.get_json()
        title = data.get("title")
        event_date = data.get("eventDate")
        start_time = data.get("startTime")
        end_time = data.get("endTime")
        location = data.get("location")
        description = data.get("description")
        user_id = data.get("userId")
        group_id = data.get("groupId")
        
        # Validate input fields
        errors = []
        if not title or title.strip() == "":
            errors.append("Title is required.")
        if not event_date:
            errors.append("Event date is required.")
        if not user_id:
            errors.append("User ID is required.")
        
        if errors:
            return jsonify({
                "status": "error",
                "message": "Validation error(s) occurred while creating the event",
                "data": [],
                "errors": errors
            }), 400
        
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "status": "error",
                "message": f"User with ID {user_id} not found",
                "data": [],
                "errors": [f"User with ID {user_id} does not exist"]
            }), 404
        
        # Create the event
        new_event = CalendarEvent(
            group_id=group_id,
            title=title,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            location=location,
            description=description,
            user_id=user_id
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Event created successfully",
            "data": new_event.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while creating the event",
            "data": [],
            "errors": [str(err)]
        }), 500


def update_event(id):
    """Update an existing event"""
    try:
        data = request.get_json()
        title = data.get("title")
        event_date = data.get("eventDate")
        start_time = data.get("startTime")
        end_time = data.get("endTime")
        location = data.get("location")
        description = data.get("description")
        
        event = CalendarEvent.query.get(id)
        
        if not event:
            return jsonify({
                "status": "error",
                "message": f"Event with id {id} not found",
                "data": [],
                "errors": [f"No event found with id {id}"]
            }), 404
        
        # Update event fields
        if title is not None:
            event.title = title
        if event_date is not None:
            event.event_date = event_date
        if start_time is not None:
            event.start_time = start_time
        if end_time is not None:
            event.end_time = end_time
        if location is not None:
            event.location = location
        if description is not None:
            event.description = description
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Event updated successfully",
            "data": event.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while updating the event",
            "data": [],
            "errors": [str(err)]
        }), 500


def delete_event(id):
    """Delete an event"""
    try:
        event = CalendarEvent.query.get(id)
        
        if not event:
            return jsonify({
                "status": "error",
                "message": f"Event with id {id} not found",
                "data": [],
                "errors": [f"No event found with id {id}"]
            }), 404
        
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Event deleted successfully",
            "data": [],
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while deleting the event",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_event_by_id(id):
    """Get a specific event by ID"""
    try:
        event = CalendarEvent.query.get(id)
        
        if not event:
            return jsonify({
                "status": "error",
                "message": f"No event found with id {id}",
                "data": [],
                "errors": [f"No event found with id {id}"]
            }), 404
        
        # Format event with user data
        event_dict = event.to_dict()
        user = User.query.get(event.user_id)
        if user:
            event_dict["user"] = {
                "id": user.id,
                "firstName": user.first_name,
                "lastName": user.last_name
            }
        
        return jsonify({
            "status": "success",
            "message": f"Event {id} found",
            "data": event_dict,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while fetching the event",
            "data": [],
            "errors": [str(err)]
        }), 500 