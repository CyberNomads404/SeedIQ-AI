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

@analyze_routes_bp.route('/get_status/<string:job_id>', methods=['GET'])
@webhook_auth_required
def analyze_get_status(job_id: str):
    http_request = HttpRequest(path_params={"job_id": job_id})
    http_response = analyze_view.get_status(http_request)
    
    return jsonify(http_response.body), http_response.status_code
