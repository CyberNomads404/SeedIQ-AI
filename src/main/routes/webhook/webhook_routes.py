from flask import Blueprint, jsonify
from src.middlewares.webhook_auth import webhook_auth_required

webhook_routes_bp = Blueprint('webhook_routes', __name__)

@webhook_routes_bp.route('/', methods=['GET'])
@webhook_auth_required
def webhook():
    return jsonify({"status": True, "message": "Webhook authenticated successfully"}), 200

@webhook_routes_bp.route('/test', methods=['POST'])
@webhook_auth_required
def webhook_test():
    

