from flask import Blueprint, jsonify, request
from src.middlewares.webhook_auth import webhook_auth_required
from src.views.http_types.http_request import HttpRequest
from src.validators.analyze_validator import analyze_validator
from src.views.analyze_view import AnalyzeView

analyze_routes_bp = Blueprint('analyze_routes', __name__)

analyze_view = AnalyzeView()

@analyze_routes_bp.route('/enqueue', methods=['POST'])
@webhook_auth_required
def analyze_enqueue():
    analyze_validator(request)
    
    http_request = HttpRequest(body=request.json)
    http_response = analyze_view.enqueue(http_request)
    
    return jsonify(http_response.body), http_response.status_code

@analyze_routes_bp.route('/get_status', methods=['GET'])
@webhook_auth_required
def analyze_get_status():
    http_request = HttpRequest(query_params=request.args)
    http_response = analyze_view.get_status(http_request)
    
    return jsonify(http_response.body), http_response.status_code
