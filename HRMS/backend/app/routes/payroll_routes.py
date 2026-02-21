from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import get_db
from app.services.payroll_service import PayrollService
from app.utils.decorators import company_required
from app.utils.rbac import role_required


payroll_bp = Blueprint(
    "payroll",
    __name__,
    url_prefix="/api/payroll"
)


# =========================
# PAID DAYS (P7.2)
# =========================
@payroll_bp.route("/<int:company_id>/paid-days", methods=["POST"])
@jwt_required()
@company_required
@role_required([1, 3])  # Admin + Finance
def upsert_paid_days(company_id):
    payload = request.get_json() or {}
    performed_by = int(get_jwt_identity())

    required_fields = ["employee_id", "payroll_year", "payroll_month", "paid_days"]

    for field in required_fields:
        if field not in payload:
            return jsonify({"error": f"{field} is required"}), 400

    with get_db() as db:
        payroll_id = PayrollService.upsert_paid_days(
            db=db,
            company_id=company_id,
            employee_id=payload["employee_id"],
            payroll_year=payload["payroll_year"],
            payroll_month=payload["payroll_month"],
            paid_days=payload["paid_days"],
            performed_by=performed_by
        )

    return jsonify({
        "message": "Paid days saved successfully",
        "payroll_id": payroll_id
    }), 200


# =========================
# GENERATE PAYROLL (P7.3)
# =========================
@payroll_bp.route("/<int:company_id>/generate", methods=["POST"])
@jwt_required()
@company_required
@role_required([1, 3])  # Admin + Finance
def generate_payroll(company_id):
    payload = request.get_json() or {}
    performed_by = int(get_jwt_identity())

    required_fields = ["employee_id", "payroll_year", "payroll_month"]

    for field in required_fields:
        if field not in payload:
            return jsonify({"error": f"{field} is required"}), 400

    with get_db() as db:
        payroll_id = PayrollService.generate_payroll(
            db=db,
            company_id=company_id,
            employee_id=payload["employee_id"],
            payroll_year=payload["payroll_year"],
            payroll_month=payload["payroll_month"],
            performed_by=performed_by
        )

    return jsonify({
        "message": "Payroll generated successfully",
        "payroll_id": payroll_id
    }), 200


# =========================
# PAYROLL BREAKUP (P7.8)
# =========================
@payroll_bp.route("/<int:company_id>/breakup", methods=["GET"])
@jwt_required()
@company_required
@role_required([1, 3])  # Admin + Finance
def get_payroll_breakup(company_id):

    employee_id = request.args.get("employee_id")
    year = request.args.get("year")
    month = request.args.get("month")

    if not employee_id or not year or not month:
        return jsonify({
            "error": "employee_id, year and month are required"
        }), 400

    with get_db() as db:
        data = PayrollService.get_payroll_breakup(
            db=db,
            company_id=company_id,
            employee_id=int(employee_id),
            payroll_year=int(year),
            payroll_month=int(month)
        )

    return jsonify(data), 200


# =========================
# LOCK PAYROLL (P7.4)
# =========================
@payroll_bp.route("/<int:company_id>/lock", methods=["POST"])
@jwt_required()
@company_required
@role_required([1, 3])  # Admin + Finance
def lock_payroll(company_id):
    payload = request.get_json() or {}
    performed_by = int(get_jwt_identity())

    required_fields = ["employee_id", "payroll_year", "payroll_month"]

    for field in required_fields:
        if field not in payload:
            return jsonify({"error": f"{field} is required"}), 400

    with get_db() as db:
        payroll_id = PayrollService.lock_payroll(
            db=db,
            company_id=company_id,
            employee_id=payload["employee_id"],
            payroll_year=payload["payroll_year"],
            payroll_month=payload["payroll_month"],
            performed_by=performed_by
        )

    return jsonify({
        "message": "Payroll locked successfully",
        "payroll_id": payroll_id
    }), 200
