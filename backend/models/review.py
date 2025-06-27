from db import db
from sqlalchemy import Enum
import enum

# Define the enum for reviewType
class ReviewType(enum.Enum):
    user = "user"
    property = "property"

class Review(db.Model):
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    review_type = db.Column(Enum(ReviewType), nullable=False)
    reviewed_item_id = db.Column(db.Integer, nullable=False)
    reviewer_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "reviewId": self.review_id,
            "reviewType": self.review_type.value,
            "reviewedItemId": self.reviewed_item_id,
            "reviewerId": self.reviewer_id,
            "score": self.score,
            "description": self.description
        }
