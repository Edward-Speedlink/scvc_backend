from flask import Blueprint, jsonify, request, abort
from ..controllers.dashboard_controller import dashboard_summary, certificates_table
from flasgger import swag_from
from ..extensions import db
from ..models.certificate import Certificate



dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/dashboard")

@dashboard_bp.get("/summary")
@swag_from({
    "tags": ["Dashboard"],
    "summary": "Get dashboard summary",
    "description": "Returns dashboard metrics such as certificate counts, verifications, etc.",
    "responses": {
        "200": {
            "description": "Dashboard summary retrieved successfully"
        }
    }
})
def summary():
    return jsonify(dashboard_summary())



@dashboard_bp.get("/certificates")
@swag_from({
    "tags": ["Dashboard"],
    "summary": "Get certificates table",
    "description": "Returns paginated list of certificates with edit/delete IDs",
    "parameters": [
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 1
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 10
        }
    ],
    "responses": {
        "200": {"description": "Paginated certificates retrieved successfully"}
    }
})
def certificates():
    return jsonify(certificates_table())


@dashboard_bp.put("/certificate/<int:cert_id>")
@swag_from({
    "tags": ["Dashboard"],
    "summary": "Edit a certificate",
    "description": "Updates student_name, course_name, or other fields of a certificate",
    "parameters": [
        {"name": "cert_id", "in": "path", "type": "integer", "required": True},
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "student_name": {"type": "string"},
                    "course_name": {"type": "string"},
                    "pdf_url": {"type": "string"},
                    "image_url": {"type": "string"},
                    "is_active": {"type": "boolean"}
                }
            }
        }
    ],
    "responses": {
        "200": {"description": "Certificate updated successfully"},
        "404": {"description": "Certificate not found"}
    }
})
def edit_certificate(cert_id):
    cert = Certificate.query.get(cert_id)
    if not cert:
        abort(404, description="Certificate not found")

    data = request.json
    for field in ["student_name", "course_name", "pdf_url", "image_url", "is_active"]:
        if field in data:
            setattr(cert, field, data[field])

    db.session.commit()
    return jsonify({"message": "Certificate updated successfully"})


@dashboard_bp.delete("/certificate/<int:cert_id>")
@swag_from({
    "tags": ["Dashboard"],
    "summary": "Delete a certificate",
    "description": "Deletes a certificate by ID",
    "parameters": [
        {"name": "cert_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        "200": {"description": "Certificate deleted successfully"},
        "404": {"description": "Certificate not found"}
    }
})
def delete_certificate(cert_id):
    cert = Certificate.query.get(cert_id)
    if not cert:
        abort(404, description="Certificate not found")

    db.session.delete(cert)
    db.session.commit()
    return jsonify({"message": "Certificate deleted successfully"})
