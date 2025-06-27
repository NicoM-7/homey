from db import db

class List(db.Model):
    __tablename__ = 'list'

    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    list_name = db.Column(db.String(255), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "listId": self.list_id,
            "userId": self.user_id,
            "listName": self.list_name,
            "groupId": self.group_id
        }
