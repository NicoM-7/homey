from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from models import Store
from db import db


def get_store_entries():
    """Get all store entries"""
    try:
        filters = dict(request.args)
        stores = Store.query.filter_by(**filters).all()
        
        if not stores:
            return jsonify({
                "status": "error",
                "message": "No store entries found",
                "data": [],
                "errors": [f"No store entries found with data {filters}"]
            }), 404
        
        result = [store.to_dict() for store in stores]
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} store entries found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to get store entries",
            "data": [],
            "errors": [str(err)]
        }), 500


def create_store_entry():
    """Create a new store entry"""
    try:
        data = request.get_json()
        item_name = data.get("itemName")
        store = data.get("store")
        price = data.get("price")
        store_link = data.get("storeLink")
        
        new_store = Store(
            item_name=item_name,
            store=store,
            price=price,
            store_link=store_link
        )
        
        db.session.add(new_store)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "New Store Created",
            "data": new_store.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while trying to create the store entry",
            "data": [],
            "errors": [str(err)]
        }), 500 