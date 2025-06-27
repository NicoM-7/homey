from flask import request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from models import Expense, Group, User
from db import db


def add_expense():
    """Add an expense to a group"""
    try:
        data = request.get_json()
        expense_name = data.get("expenseName")
        group_id = data.get("groupId")
        amount = data.get("amount")
        owed_to = data.get("owedTo")
        paid_by = data.get("paidBy")
        
        # Validate required fields
        if not all([expense_name, group_id, amount, owed_to, paid_by]):
            return jsonify({
                "status": "error",
                "message": "Missing required fields",
                "data": [],
                "errors": ["expenseName, groupId, amount, owedTo, and paidBy are required"]
            }), 400
        
        # Ensure the group exists
        group = Group.query.get(group_id)
        if not group:
            return jsonify({
                "status": "error",
                "message": "Group not found",
                "data": [],
                "errors": [f"No group found with ID {group_id}"]
            }), 404
        
        # Create the expense
        expense = Expense(
            group_id=group_id,
            expense_name=expense_name,
            amount=amount,
            owed_to=owed_to,
            paid_by=paid_by,
            completed=False
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Expense added successfully",
            "data": expense.to_dict(),
            "errors": []
        }), 201
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Failed to add expense",
            "data": [],
            "errors": [str(err)]
        }), 500


def get_expenses(group_id):
    """Get all expenses for a group"""
    try:
        # Validate group_id
        try:
            group_id = int(group_id)
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Invalid group ID",
                "data": [],
                "errors": ["Group ID must be a number"]
            }), 400
        
        # Build filter conditions
        filters = {"group_id": group_id}
        
        # Add optional filters from query parameters
        owed_to = request.args.get("owedTo")
        if owed_to:
            try:
                filters["owed_to"] = int(owed_to)
            except ValueError:
                pass
        
        paid_by = request.args.get("paidBy")
        if paid_by:
            try:
                filters["paid_by"] = int(paid_by)
            except ValueError:
                pass
        
        # Retrieve expenses with user relationships
        expenses = Expense.query.filter_by(**filters).all()
        
        if not expenses:
            return jsonify({
                "status": "error",
                "message": "No expenses found matching the provided criteria",
                "data": [],
                "errors": [f"No expenses found for group ID {group_id}"]
            }), 404
        
        # Format response with user details
        result = []
        for expense in expenses:
            expense_dict = expense.to_dict()
            
            # Get user details for owed_to and paid_by
            owed_to_user = User.query.get(expense.owed_to)
            paid_by_user = User.query.get(expense.paid_by)
            
            expense_dict["owed_to_user"] = owed_to_user.to_safe_dict() if owed_to_user else None
            expense_dict["paid_by_user"] = paid_by_user.to_safe_dict() if paid_by_user else None
            
            result.append(expense_dict)
        
        return jsonify({
            "status": "success",
            "message": f"{len(result)} expense(s) found",
            "data": result,
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve expenses",
            "data": [],
            "errors": [str(err)]
        }), 500


def complete_expense(id):
    """Mark an expense as completed"""
    try:
        expense = Expense.query.get(id)
        
        if not expense:
            return jsonify({
                "status": "error",
                "message": "Expense not found",
                "data": [],
                "errors": [f"Expense with id {id} not found"]
            }), 404
        
        expense.completed = True
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Expense marked as completed",
            "data": expense.to_dict(),
            "errors": []
        }), 200
        
    except SQLAlchemyError as err:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred while completing the expense",
            "data": [],
            "errors": [str(err)]
        }), 500 