from flask import Blueprint, jsonify
from src.middlewares.webhook_auth import webhook_auth_required
from .analyze.analyze_routes import analyze_routes_bp

webhook_routes_bp = Blueprint('webhook_routes', __name__)

@webhook_routes_bp.route('/', methods=['GET'])
@webhook_auth_required
def webhook():
    return jsonify({
        "status": True, 
        "message": "Webhook authenticated successfully",
        "data": None,
    }), 200

webhook_routes_bp.register_blueprint(analyze_routes_bp, url_prefix='/analyze')
