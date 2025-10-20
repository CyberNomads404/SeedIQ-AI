import os
from functools import wraps
from flask import request
from dotenv import load_dotenv

# Importa as exceções
from src.errors.error_types.http_unauthorized import HttpUnauthorizedError
from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

load_dotenv()

def webhook_auth_required(f):
    """
        Middleware to validate the webhook token in incoming requests
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise HttpUnauthorizedError(
                message='Authorization header is required'
            )

        try:
            token_type, token = auth_header.split(' ')
            if token_type.lower() != 'bearer':
                raise HttpBadRequestError(
                    message='Invalid token format. Use: Bearer {token}'
                )
        except ValueError:
            raise HttpBadRequestError(
                message='Invalid token format. Use: Bearer {token}'
            )

        expected_token = os.getenv('WEBHOOK_RECEIVE_TOKEN')

        if not expected_token:
            raise HttpUnprocessableEntityError(
                message='WEBHOOK_RECEIVE_TOKEN not configured in environment'
            )

        if token != expected_token:
            raise HttpUnauthorizedError(
                message='Unauthorized authentication token'
            )

        return f(*args, **kwargs)

    return decorated_function
