from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import os

db = SQLAlchemy()

def init_db(app):
    db_url = os.getenv("DB_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def sync_database():
    with current_app.app_context():
        db.create_all()