from db import db

class Item(db.Model):
    __tablename__ = 'item'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    list_id = db.Column(db.Integer, nullable=False)
    item = db.Column(db.String(255), nullable=False)
    assigned_to = db.Column(db.String(255), nullable=True)
    purchased = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "itemId": self.item_id,
            "listId": self.list_id,
            "item": self.item,
            "assignedTo": self.assigned_to,
            "purchased": self.purchased
        }
