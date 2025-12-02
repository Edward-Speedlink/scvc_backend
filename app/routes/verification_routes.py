from flask import Blueprint, jsonify, request 
from ..controllers.verification_controller import verify_certificate
from flasgger import swag_from


verification_bp = Blueprint('verification_bp', __name__, url_prefix='/certificate')


@verification_bp.get('/<path:code>')
@swag_from({
    "tags": ["Verification"],
    "summary": "Verify a certificate",
    "description": "Checks if a certificate is valid by verification code.",
    "parameters": [
        {
            "name": "code",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Certificate verification code (can contain slashes)"
        }
    ],
    "responses": {
        "200": {"description": "Verification result returned"},
        "404": {"description": "Certificate not found"}
    }
})
def verify(code):
    try:
        result = verify_certificate(code)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "ERROR", 
            "message": f"Internal server error: {str(e)}"
        }), 500
    
# @verification_bp.get('/<code>')
# @swag_from({
#     "tags": ["Verification"],
#     "summary": "Verify a certificate",
#     "description": "Checks if a certificate is valid by verification code.",
#     "parameters": [
#         {
#             "name": "code",
#             "in": "path",
#             "type": "string",
#             "required": True,
#             "description": "Certificate verification code"
#         }
#     ],
#     "responses": {
#         "200": {"description": "Verification result returned"},
#         "404": {"description": "Certificate not found"}
#     }
# })
# def verify(code):
#     try:
#         result = verify_certificate(code)
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({
#             "status": "ERROR", 
#             "message": f"Internal server error: {str(e)}"
#         }), 500


# --- POST route (code in JSON body) ---
@verification_bp.post('/verify')
@swag_from({
    "tags": ["Verification"],
    "summary": "Verify a certificate (POST)",
    "description": "Checks if a certificate is valid by sending JSON body with certificate code.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "certificate_code": {"type": "string"}
                },
                "required": ["certificate_code"]
            }
        }
    ],
    "responses": {
        "200": {"description": "Verification result returned"},
        "400": {"description": "Certificate code not provided"},
        "404": {"description": "Certificate not found"}
    }
})
def verify_post():
    try:
        data = request.get_json()
        if not data or "certificate_code" not in data:
            return jsonify({"error": "certificate_code is required"}), 400

        code = data["certificate_code"]
        result = verify_certificate(code)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": f"Internal server error: {str(e)}"
        }), 500
    
# def verify_post():
#     data = request.get_json()
#     if not data or "certificate_code" not in data:
#         return jsonify({"error": "certificate_code is required"}), 400

#     code = data["certificate_code"]
#     result = verify_certificate(code)
#     return jsonify(result)
