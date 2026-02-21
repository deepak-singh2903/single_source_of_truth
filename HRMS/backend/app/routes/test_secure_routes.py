from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.utils.decorators import company_required
from app.utils.rbac import role_required


test_secure_bp = Blueprint(
    "test_secure",
    __name__,
    url_prefix="/test-secure"
)


# ====================================================
# ADMIN + COMPANY VALIDATION TEST ENDPOINT
# ====================================================
@test_secure_bp.route("/companies/<int:company_id>/admin-check", methods=["GET"])
@jwt_required()
@company_required
@role_required([1])   # Admin only
def admin_company_check(company_id):
    """
    Test endpoint to verify:
    - JWT validity
    - Company isolation
    - Admin role enforcement
    """

    try:
        return jsonify({
            "message": "Access granted",
            "company_id": company_id
        }), 200

    except Exception as exc:
        print("🔥 TEST SECURE ERROR:", exc)
        return jsonify({
            "error": "Access denied"
        }), 403
