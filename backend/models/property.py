from db import db
from sqlalchemy import Enum, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import base64

# Property type enum
class PropertyType(enum.Enum):
    House = "House"
    Apartment = "Apartment"
    Condo = "Condo"
    Townhouse = "Townhouse"
    Duplex = "Duplex"
    Studio = "Studio"
    Loft = "Loft"
    Bungalow = "Bungalow"
    Cabin = "Cabin"
    MobileHome = "Mobile Home"
    Other = "Other"

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    property_description = db.Column(db.Text, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    property_type = db.Column(Enum(PropertyType), nullable=False)
    availability = db.Column(db.Boolean, default=True, nullable=False)

    landlord_id = db.Column(db.Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    exterior_image = db.Column(LargeBinary(length=2**32 - 1), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Optional relationship if you want to backref to User
    landlord = relationship("User", back_populates="properties")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "propertyDescription": self.property_description,
            "bedrooms": self.bedrooms,
            "price": self.price,
            "propertyType": self.property_type.value,
            "availability": self.availability,
            "landlordId": self.landlord_id,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "exteriorImage": base64.b64encode(self.exterior_image).decode('utf-8') if self.exterior_image else None
        }
