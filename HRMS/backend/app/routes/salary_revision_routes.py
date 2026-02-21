from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import get_db
from app.services.salary_revision_service import SalaryRevisionService
from app.utils.decorators import company_required
from app.utils.rbac import role_required


salary_bp = Blueprint(
    "salary_revisions",
    __name__,
    url_prefix="/api/salary-revisions"
)


# =====================================
# APPLY SALARY REVISION (POST)
# =====================================
@salary_bp.route("/<int:company_id>/<int:employee_id>", methods=["POST"])
@jwt_required()
@company_required
@role_required([1])  # Admin only
def apply_salary_revision(company_id, employee_id):
    payload = request.get_json() or {}
    performed_by = int(get_jwt_identity())

    if not payload:
        return jsonify({"error": "Request payload is required"}), 400

    try:
        with get_db() as db:
            revision_id = SalaryRevisionService.apply_salary_revision(
                db=db,
                company_id=company_id,
                employee_id=employee_id,
                payload=payload,
                performed_by=performed_by
            )

        return jsonify({
            "message": "Salary revision applied successfully",
            "salary_revision_id": revision_id
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as exc:
        print("🔥 SALARY REVISION ERROR:", exc)
        return jsonify({
            "error": "Internal server error"
        }), 500


# =====================================
# SALARY REVISION HISTORY (GET)
# =====================================
@salary_bp.route("/<int:company_id>/<int:employee_id>", methods=["GET"])
@jwt_required()
@company_required
@role_required([1, 2])  # Admin + HR
def get_salary_revision_history(company_id, employee_id):
    try:
        with get_db() as db:
            history = SalaryRevisionService.get_salary_revision_history(
                db=db,
                company_id=company_id,
                employee_id=employee_id
            )

        return jsonify(history), 200

    except Exception as exc:
        print("🔥 SALARY HISTORY ERROR:", exc)
        return jsonify({
            "error": "Internal server error"
        }), 500
