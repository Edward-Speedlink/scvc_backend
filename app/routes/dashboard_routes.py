from flask import Blueprint, jsonify
from ..controllers.dashboard_controller import dashboard_summary
from flasgger import swag_from


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
