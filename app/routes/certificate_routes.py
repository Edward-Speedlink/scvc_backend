from flask import Blueprint, request, jsonify
from ..controllers.certificate_controller import create_certificate
from flasgger import swag_from


certificate_bp = Blueprint('certificate_bp', __name__, url_prefix='/certificate')

@certificate_bp.post('/create')
@swag_from({
    "tags": ["Certificates"],
    "summary": "Create a certificate",
    "description": "Creates a certificate, generates a verification code and PDF file.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "student_name": {"type": "string"},
                    "course_name": {"type": "string"}
                },
                "required": ["student_name", "course_name"]
            }
        }
    ],
    "responses": {
        "200": {"description": "Certificate created successfully"},
        "400": {"description": "Invalid input"}
    }
})
def create_cert():
    data = request.json
    result = create_certificate(data)
    return jsonify(result)
