from db import db
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from datetime import datetime

class Chore(db.Model):
    __tablename__ = 'Chores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    chore_name = db.Column(db.String(255), nullable=False)
    room = db.Column(db.String(255), nullable=False)

    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    banner_image = db.Column(db.String(255), nullable=True)

    due_date = db.Column(db.DateTime, nullable=False)

    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "choreName": self.chore_name,
            "room": self.room,
            "assignedTo": self.assigned_to,
            "completed": self.completed,
            "bannerImage": self.banner_image,
            "dueDate": self.due_date.isoformat() if self.due_date else None,
            "groupId": self.group_id
        }
