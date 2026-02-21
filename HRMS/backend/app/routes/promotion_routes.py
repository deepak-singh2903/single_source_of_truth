from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import get_db
from app.services.promotion_service import PromotionService
from app.utils.decorators import company_required
from app.utils.rbac import role_required


promotion_bp = Blueprint(
    "promotions",
    __name__,
    url_prefix="/api/promotions"
)

# --------------------------------------------------
# P5.1 – APPLY PROMOTION (WRITE)
# --------------------------------------------------
@promotion_bp.route("/<int:company_id>/<int:employee_id>", methods=["POST"])
@jwt_required()
@company_required
@role_required([1])   # Admin only
def apply_promotion(company_id, employee_id):
    """
    Apply promotion / role change (Admin only)
    """
    payload = request.get_json() or {}
    performed_by = int(get_jwt_identity())

    if not payload:
        return jsonify({"error": "Request payload is required"}), 400

    try:
        with get_db() as db:
            promotion_id = PromotionService.apply_promotion(
                db=db,
                company_id=company_id,
                employee_id=employee_id,
                payload=payload,
                performed_by=performed_by
            )

        return jsonify({
            "message": "Promotion applied successfully",
            "promotion_id": promotion_id
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as exc:
        print("🔥 PROMOTION ERROR:", exc)
        return jsonify({
            "error": "Internal server error"
        }), 500


# --------------------------------------------------
# P5.2 – PROMOTION HISTORY (READ)
# --------------------------------------------------
@promotion_bp.route("/<int:company_id>/<int:employee_id>", methods=["GET"])
@jwt_required()
@company_required
@role_required([1])   # Admin only
def get_promotion_history(company_id, employee_id):
    """
    Fetch promotion history for an employee
    """
    try:
        with get_db() as db:
            history = PromotionService.get_promotion_history(
                db=db,
                company_id=company_id,
                employee_id=employee_id
            )

        return jsonify(history), 200

    except Exception as exc:
        print("🔥 PROMOTION HISTORY ERROR:", exc)
        return jsonify({
            "error": "Internal server error"
        }), 500
