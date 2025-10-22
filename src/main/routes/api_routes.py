from flask import Blueprint, jsonify
from src.middlewares.webhook_auth import webhook_auth_required
from src.main.routes.webhook.webhook_routes import webhook_routes_bp

# Views the Routes
from src.views.api_view import ApiView

api_routes_bp = Blueprint('api_routes', __name__)

@api_routes_bp.route('/', methods=['GET'])
def home():
    api_view = ApiView()
    http_response = api_view.home()
    
    return jsonify(http_response.body), http_response.status_code

@api_routes_bp.route('/_routes', methods=['GET'])
def list_routes():
    from flask import current_app
    data = []
    for rule in current_app.url_map.iter_rules():
        data.append({
            "rule": str(rule),
            "methods": sorted(m for m in rule.methods if m not in ("HEAD", "OPTIONS")),
            "endpoint": rule.endpoint
        })
    return jsonify(data), 200

api_routes_bp.register_blueprint(webhook_routes_bp, url_prefix='/webhook')