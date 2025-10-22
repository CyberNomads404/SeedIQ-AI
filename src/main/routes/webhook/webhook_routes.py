from flask import Blueprint, jsonify, request
from src.middlewares.webhook_auth import webhook_auth_required
from src.views.http_types.http_request import HttpRequest
from src.controllers.job_controller import enqueue

webhook_routes_bp = Blueprint('webhook_routes', __name__)

@webhook_routes_bp.route('/', methods=['GET'])
@webhook_auth_required
def webhook():
    return jsonify({"status": True, "message": "Webhook authenticated successfully"}), 200

@webhook_routes_bp.route('/enqueue', methods=['POST'])
@webhook_auth_required
def webhook_enqueue():
    http_request = HttpRequest(body=request.json)
    http_response = enqueue(http_request)
    
    return jsonify(http_response.body), http_response.status_code

@webhook_routes_bp.route('/get_status', methods=['GET'])
def webhook_get_status():
    http_request = HttpRequest(query=request.args)
    http_response = enqueue(http_request)
    
    return jsonify(http_response.body), http_response.status_code
