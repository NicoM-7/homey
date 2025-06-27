from db import db
from sqlalchemy import Enum, ForeignKey
import enum

# Enums for habits
class Intensity(enum.Enum):
    none = ""
    low = "Low"
    medium = "Medium"
    high = "High"

class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    cleaning_habits = db.Column(Enum(Intensity), nullable=True)
    noise_level = db.Column(Enum(Intensity), nullable=True)

    sleep_start = db.Column(db.String(255), nullable=True)
    sleep_end = db.Column(db.String(255), nullable=True)

    alergies = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, nullable=False)  # FK to users.id (optional to enforce if no cascade needed)
    group_id = db.Column(db.Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "cleaningHabits": self.cleaning_habits.value if self.cleaning_habits else "",
            "noiseLevel": self.noise_level.value if self.noise_level else "",
            "sleepStart": self.sleep_start,
            "sleepEnd": self.sleep_end,
            "alergies": self.alergies,
            "userId": self.user_id,
            "groupId": self.group_id
        }
