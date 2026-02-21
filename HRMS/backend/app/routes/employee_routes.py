from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.database import SessionLocal
from app.models.employee_master import EmployeeMaster
from app.services.payroll_service import calculate_pf, calculate_hra
from app.utils.rbac import role_required

employee_bp = Blueprint("employee_bp", __name__)


# ===============================
# GET ALL EMPLOYEES (PROTECTED)
# ===============================
@employee_bp.route("/employees", methods=["GET"])
@jwt_required()
@role_required([1, 2])   # Admin + HR
def get_employees():
    db = SessionLocal()

    try:
        employees = db.query(EmployeeMaster).all()

        result = []

        for emp in employees:
            result.append({
                "employee_id": emp.employee_id,
                "employee_code": emp.employee_code,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "department_name_snapshot": emp.department_name_snapshot,
                "employment_status": emp.employment_status,
                "pf_scheme_type": emp.pf_scheme_type,
                "current_basic": float(emp.current_basic) if emp.current_basic else 0,
                "hra_type": emp.hra_type,
                "employment_mode": emp.employment_mode
            })

        return jsonify(result)

    finally:
        db.close()


# ===================================
# GET SINGLE EMPLOYEE DETAIL (PROTECTED)
# ===================================
@employee_bp.route("/employees/<int:employee_id>", methods=["GET"])
@jwt_required()
@role_required([1, 2])   # Admin + HR
def get_employee_detail(employee_id):
    db = SessionLocal()

    try:
        emp = db.query(EmployeeMaster).filter(
            EmployeeMaster.employee_id == employee_id
        ).first()

        if not emp:
            return {"error": "Employee not found"}, 404

        basic = float(emp.current_basic) if emp.current_basic else 0
        da = 0  # update later if DA column exists

        hra = calculate_hra(
            basic,
            emp.hra_type,
            float(emp.hra_percentage) if emp.hra_percentage else 0
        )

        pf = calculate_pf(
            basic,
            da,
            emp.pf_scheme_type
        )

        gross = basic + da + hra
        net = gross - pf

        result = {
            "employee_id": emp.employee_id,
            "employee_code": emp.employee_code,
            "name": f"{emp.first_name} {emp.last_name}",
            "department": emp.department_name_snapshot,
            "status": emp.employment_status,
            "basic": basic,
            "hra": hra,
            "pf": pf,
            "gross": gross,
            "net": net,
            "pf_scheme": emp.pf_scheme_type,
            "hra_type": emp.hra_type,
            "pay_commission": emp.pay_commission_type
        }

        return jsonify(result)

    finally:
        db.close()
