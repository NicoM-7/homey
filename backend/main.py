from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from routes.user_routes import user_routes
from routes.list_routes import list_routes
from routes.store_routes import store_routes
from routes.profile_routes import profile_routes
from routes.conversation_routes import conversation_routes
from routes.message_routes import message_routes
from routes.expense_routes import expense_routes
from routes.inventory_routes import inventory_routes
from routes.calendar_routes import calendar_routes
from routes.property_routes import property_routes
from routes.group_routes import group_routes
from routes.chores_routes import chores_routes
from routes.review_routes import review_routes
# from middleware.logger import logger
from db import db, init_db, sync_database
from dotenv import load_dotenv
from models import *
import os
import ssl

load_dotenv()

app = Flask(__name__)
init_db(app)
CORS(app)

# Logger middleware (you can uncomment this once logger is implemented)
# app.before_request(logger)

# JSON body limits (optional)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

# Register Blueprints
app.register_blueprint(user_routes, url_prefix="/api/users")
app.register_blueprint(list_routes, url_prefix="/api/lists")
app.register_blueprint(store_routes, url_prefix="/api/stores")
app.register_blueprint(profile_routes, url_prefix="/api/profile")
app.register_blueprint(conversation_routes, url_prefix="/api/conversations")
app.register_blueprint(message_routes, url_prefix="/api/messages")
app.register_blueprint(expense_routes, url_prefix="/api/expenses")
app.register_blueprint(inventory_routes, url_prefix="/api/inventory")
app.register_blueprint(calendar_routes, url_prefix="/api/calendar")
app.register_blueprint(property_routes, url_prefix="/api/properties")
app.register_blueprint(group_routes, url_prefix="/api/groups")
app.register_blueprint(chores_routes, url_prefix="/api/chores")
app.register_blueprint(review_routes, url_prefix="/api/reviews")

# Health check route
@app.route("/")
def index():
    return jsonify({ "message": "Backend is running" })

# 404 Handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({ "message": f"{request.method} {request.path} Not found" }), 404

def run_http(port):
    with app.app_context():
        if os.getenv("SYNC") == "true":
            sync_database()
            print("Database synced")
    app.run(host="0.0.0.0", port=port)

def run_https(port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./cert.crt', './key.pem')
    app.run(host="0.0.0.0", port=port, ssl_context=context)

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 8080))
    if os.getenv("DEVELOPMENT", "true") == "true":
        run_http(port)
    else:
        run_https(port)