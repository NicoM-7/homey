from db import db
from sqlalchemy.orm import relationship

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', ondelete='SET NULL'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "landlordId": self.landlord_id,
            "propertyId": self.property_id
        }
