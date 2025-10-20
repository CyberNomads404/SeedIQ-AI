from flask import Flask
from flask_cors import CORS
from src.errors.error_handler import error_handler

# Routes
from src.main.routes.app_routes import app_routes_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(app_routes_bp)

@app.errorhandler(Exception)
def handle_error(e):
    response = error_handler(e)
    return response.body, response.status_code