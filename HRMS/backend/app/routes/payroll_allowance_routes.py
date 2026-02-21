from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.database import get_db
from app.services.payroll_allowance_service import PayrollAllowanceService
from app.utils.decorators import company_required
from app.utils.rbac import role_required


allowance_bp = Blueprint(
    "payroll_allowances",
    __name__,
    url_prefix="/api/payroll-allowances"
)


# --------------------------------------------------
# UPSERT ALLOWANCE (WRITE)
# --------------------------------------------------
@allowance_bp.route("/<int:company_id>", methods=["POST"])
@jwt_required()
@company_required
@role_required([1])   # Admin only
def upsert_allowance(company_id):

    payload = request.get_json() or {}

    if not payload:
        return jsonify({"error": "Request payload is required"}), 400

    required_fields = [
        "allowance_code",
        "calculation_type",
        "calculation_value"
    ]

    for field in required_fields:
        if field not in payload:
            return jsonify({"error": f"{field} is required"}), 400

    try:
        with get_db() as db:
            allowance_id = PayrollAllowanceService.upsert_allowance(
                db=db,
                company_id=company_id,
                allowance_code=payload["allowance_code"],
                calculation_type=payload["calculation_type"],
                calculation_value=payload["calculation_value"]
            )

        return jsonify({
            "message": "Allowance saved successfully",
            "allowance_id": allowance_id
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as exc:
        print("🔥 PAYROLL ALLOWANCE ERROR:", exc)
        return jsonify({
            "error": "Internal server error"
        }), 500
