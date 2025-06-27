from db import db
from sqlalchemy import ForeignKey

class CalendarEvent(db.Model):
    __tablename__ = "calendar_events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    # Title of the event
    title = db.Column(db.String(255), nullable=False)

    # Date of the event
    event_date = db.Column(db.Date, nullable=False)

    # Optional times
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)

    # Optional location and description
    location = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Group association
    group_id = db.Column(db.Integer, ForeignKey('groups.id', ondelete="CASCADE"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "eventDate": self.event_date.isoformat() if self.event_date else None,
            "startTime": self.start_time.isoformat() if self.start_time else None,
            "endTime": self.end_time.isoformat() if self.end_time else None,
            "location": self.location,
            "description": self.description,
            "groupId": self.group_id
        }
