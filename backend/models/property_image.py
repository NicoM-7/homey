from db import db
from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
import base64

class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    property_id = db.Column(db.Integer, ForeignKey('properties.id', ondelete='CASCADE'), nullable=False)

    label = db.Column(db.String(255), nullable=False)
    image = db.Column(LargeBinary(length=2**32 - 1), nullable=False)
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Optional relationship (one image belongs to one property)
    property = relationship("Property", back_populates="images")

    def to_dict(self):
        return {
            "id": self.id,
            "propertyId": self.property_id,
            "label": self.label,
            "image": base64.b64encode(self.image).decode("utf-8") if self.image else None,
            "description": self.description,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }
