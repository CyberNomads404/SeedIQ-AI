import os
from flask import Blueprint, request, jsonify, send_from_directory

# Views the Routes
from src.views.app_view import AppView

app_routes_bp = Blueprint('app_routes', __name__)

@app_routes_bp.route('/', methods=['GET'])
def home():
    app_view = AppView()
    http_response = app_view.home()
    
    return jsonify(http_response.body), http_response.status_code

@app_routes_bp.route('/docs')
def swagger_ui():
    return send_from_directory(os.path.join(app_routes_bp.root_path, '../../templates'),
                          'docs.html')

@app_routes_bp.route('/openapi.json')
def swagger():
    return send_from_directory(os.path.join(app_routes_bp.root_path, '../../templates/documentation'),
                          'openapi.json')

@app_routes_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app_routes_bp.root_path, '../../static'),
                          'favicon.ico')
