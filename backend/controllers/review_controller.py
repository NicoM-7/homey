from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import Review
from db import db


def get_reviews():
    """Get reviews based on query parameters"""
    try:
        filters = dict(request.args)
        
        reviews = Review.query.filter_by(**filters).order_by(Review.created_at).all()
        
        if not reviews:
            return jsonify({
                "status": "error",
                "message": "There are no reviews for the selected item",
                "data": [],
                "errors": [f"No reviews found with data {filters}"]
            }), 404
        
        result = [review.to_dict() for review in reviews]
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} reviews found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to get the reviews",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_review():
    """Create a new review"""
    try:
        data = request.get_json()
        review_type = data.get("reviewType")
        reviewed_item_id = data.get("reviewedItemId")
        reviewer_id = data.get("reviewerId")
        score = data.get("score")
        description = data.get("description")
        
        # Check if the reviewer has already reviewed this item
        existing_review = Review.query.filter_by(
            review_type=review_type,
            reviewed_item_id=reviewed_item_id,
            reviewer_id=reviewer_id
        ).first()
        
        if existing_review:
            return jsonify({
                "status": "error",
                "message": "The user has already created a review for this item",
                "data": [],
                "errors": ["A review already exists for this user and item"]
            }), 400
        
        new_review = Review(
            review_type=review_type,
            reviewed_item_id=reviewed_item_id,
            reviewer_id=reviewer_id,
            score=score,
            description=description
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Review created",
            "data": new_review.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to create the review",
            "data": [],
            "errors": [str(err)]
        }), 500 