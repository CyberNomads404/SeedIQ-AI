from flask import Blueprint, jsonify
from src.middlewares.webhook_auth import webhook_auth_required

# Views the Routes
from src.views.api_view import ApiView

api_routes_bp = Blueprint('api_routes', __name__)

@api_routes_bp.route('/', methods=['GET'])
def home():
    api_view = ApiView()
    http_response = api_view.home()
    
    return jsonify(http_response.body), http_response.status_code

@api_routes_bp.route('/webhook', methods=['GET'])
@webhook_auth_required
def webhook():
    return jsonify({"status": True, "message": "Webhook authenticated successfully"}), 200