from cerberus import Validator
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from .request_json_validator import request_json_validator

def analyze_validator(request: any) -> None:
    request_json_validator(request)

    body_validator = Validator({
        "callback_url": {"type": "string", "required": True, "empty": False},
        "payload": {
            "type": "dict",
            "required": True,
            "empty": False,
            "schema": {
                "external_id": {"type": "string", "required": True, "empty": False},
                "image_url": {"type": "string", "required": True, "empty": False},
                "seed_category": {"type": "string", "required": True, "empty": False},
            },
        },
    })

    if not body_validator.validate(request.json):
        raise HttpUnprocessableEntityError(body_validator.errors)
