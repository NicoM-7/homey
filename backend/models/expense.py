from db import db
from sqlalchemy import Float, Boolean
from sqlalchemy.orm import relationship

class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expense_name = db.Column(db.String(255), nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(Float, nullable=False)

    paid_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owed_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    completed = db.Column(Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "expenseName": self.expense_name,
            "groupId": self.group_id,
            "amount": self.amount,
            "paidBy": self.paid_by,
            "owedTo": self.owed_to,
            "completed": self.completed
        }
