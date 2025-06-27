from db import db

class Store(db.Model):
    __tablename__ = "store"

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    store = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    store_link = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "itemID": self.item_id,
            "itemName": self.item_name,
            "store": self.store,
            "price": self.price,
            "storeLink": self.store_link
        }
