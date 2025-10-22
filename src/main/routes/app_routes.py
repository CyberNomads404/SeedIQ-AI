import os
from flask import Blueprint, send_from_directory

from src.main.routes.api_routes import api_routes_bp

app_routes_bp = Blueprint('app_routes', __name__)

@app_routes_bp.route('/')
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

app_routes_bp.register_blueprint(api_routes_bp, url_prefix='/api')