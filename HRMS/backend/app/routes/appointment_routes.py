from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import get_db
from app.services.appointment_service import AppointmentService
from app.utils.decorators import company_required
from app.utils.rbac import role_required


appointment_bp = Blueprint(
    "appointments",
    __name__,
    url_prefix="/api/appointments"
)


# --------------------------------------------------
# CREATE APPOINTMENT (WRITE)
# --------------------------------------------------
@appointment_bp.route("/<int:company_id>/<int:employee_id>", methods=["POST"])
@jwt_required()
@company_required
@role_required([1])   # Admin only
def create_appointment(company_id, employee_id):
    """
    Create new employee appointment (Admin only)
    """

    payload = request.get_json() or {}
    performed_by = int(get_jwt_identity())

    if not payload:
        return jsonify({"error": "Request payload is required"}), 400

    try:
        with get_db() as db:
            appointment = AppointmentService.create_appointment(
                db=db,
                company_id=company_id,
                employee_id=employee_id,
                payload=payload,
                performed_by=performed_by
            )

        return jsonify({
            "message": "Appointment created successfully",
            "appointment_id": appointment.appointment_id
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as exc:
        print("🔥 APPOINTMENT ERROR:", exc)
        return jsonify({
            "error": "Internal server error"
        }), 500
