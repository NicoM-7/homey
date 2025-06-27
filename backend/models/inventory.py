from db import db

class Inventory(db.Model):
    __tablename__ = 'inventory'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            "itemId": self.item_id,
            "itemName": self.item_name,
            "quantity": self.quantity,
            "groupId": self.group_id
        }
