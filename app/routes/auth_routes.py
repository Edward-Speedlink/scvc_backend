from flask import Blueprint, request, jsonify
from ..controllers.auth_controller import register_user, login_user
from flasgger import swag_from

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.post('/register')
@swag_from({
    "tags": ["Auth"],
    "summary": "Register a new user",
    "description": "Creates a new user account using email, password, and optional role.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "role": {"type": "string"}
                },
                "required": ["email", "password"]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "User registered successfully"
        },
        "400": {
            "description": "Validation error"
        }
    }
})
def register():
    data = request.json
    result = register_user(data)
    return jsonify(result)

@auth_bp.post('/login')
@swag_from({
    "tags": ["Auth"],
    "summary": "Login a user",
    "description": "Authenticates a user with email and password and returns a JWT token.",
    "consumes": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "password": {"type": "string"}
                },
                "required": ["email", "password"]
            }
        }
    ],
    "responses": {
        "200": {"description": "Login successful"},
        "401": {"description": "Invalid credentials"}
    }
})
def login():
    data = request.json
    result = login_user(data)
    return jsonify(result)
