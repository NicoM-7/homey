from db import db
from datetime import datetime

class GroupParticipant(db.Model):
    __tablename__ = 'group_participant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "groupId": self.group_id,
            "tenantId": self.tenant_id,
            "joinedAt": self.joined_at.isoformat() if self.joined_at else None
        }
