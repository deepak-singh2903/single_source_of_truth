from datetime import date

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.database import get_db
from app.services.pay_commission_service import PayCommissionService
from app.utils.decorators import company_required
from app.utils.rbac import role_required


pay_commission_bp = Blueprint(
    "pay_commission_policy",
    __name__,
    url_prefix="/api/policies/pay-commission"
)


# ======================================================
# LIST ALL PAY COMMISSION POLICIES
# ======================================================
@pay_commission_bp.route("/<int:company_id>", methods=["GET"])
@jwt_required()
@company_required
@role_required([1])   # Admin only
def list_pay_commission_policies(company_id):
    """
    Admin / HR can view all CPC policies.
    company_id validated by decorator.
    """

    try:
        with get_db() as db:
            policies = PayCommissionService.list_all_policies(db=db)

        return jsonify([
            {
                "policy_id": p.policy_id,
                "pay_commission": p.pay_commission,
                "da_percent": float(p.da_percent),
                "effective_from": str(p.effective_from),
                "effective_to": str(p.effective_to) if p.effective_to else None,
                "is_active": p.is_active
            }
            for p in policies
        ]), 200

    except Exception as exc:
        print("🔥 PAY COMMISSION LIST ERROR:", exc)
        return jsonify({"error": "Internal server error"}), 500


# ======================================================
# UPDATE DA % (VERSIONED — SAFE)
# ======================================================
@pay_commission_bp.route(
    "/<int:company_id>/<int:policy_id>/update-da",
    methods=["POST"]
)
@jwt_required()
@company_required
@role_required([1])   # Admin only
def update_da_percent(company_id, policy_id):

    payload = request.get_json() or {}

    required_fields = ["da_percent", "effective_from"]

    for f in required_fields:
        if f not in payload:
            return jsonify({"error": f"{f} is required"}), 400

    try:
        with get_db() as db:
            new_policy_id = PayCommissionService.update_da_percent(
                db=db,
                company_id=company_id,
                policy_id=policy_id,
                new_da_percent=float(payload["da_percent"]),
                effective_from=date.fromisoformat(payload["effective_from"])
            )

        return jsonify({
            "message": "DA percentage updated successfully",
            "new_policy_id": new_policy_id
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as exc:
        print("🔥 UPDATE DA ERROR:", exc)
        return jsonify({"error": "Internal server error"}), 500


# ======================================================
# ACTIVATE / DEACTIVATE PAY COMMISSION
# ======================================================
@pay_commission_bp.route(
    "/<int:company_id>/<int:policy_id>/status",
    methods=["POST"]
)
@jwt_required()
@company_required
@role_required([1])   # Admin only
def set_pay_commission_status(company_id, policy_id):

    payload = request.get_json() or {}

    if "is_active" not in payload:
        return jsonify({"error": "is_active is required"}), 400

    try:
        with get_db() as db:
            PayCommissionService.set_policy_status(
                db=db,
                policy_id=policy_id,
                is_active=bool(payload["is_active"])
            )

        return jsonify({
            "message": "Pay Commission status updated"
        }), 200

    except Exception as exc:
        print("🔥 STATUS UPDATE ERROR:", exc)
        return jsonify({"error": "Internal server error"}), 500
