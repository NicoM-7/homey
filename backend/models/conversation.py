from db import db
from sqlalchemy import Enum

class Conversation(db.Model):
    __tablename__ = 'conversation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(Enum("dm", "group", name="conversation_type"), nullable=False)
    name = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "groupId": self.group_id,
            "type": self.type,
            "name": self.name
        }
