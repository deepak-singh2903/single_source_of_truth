from sqlalchemy.orm import Session

from app.models.employee_master import EmployeeMaster
from app.models.appointment_form import AppointmentForm
from app.models.audit_log import AuditLog

from app.services.appointment_validator import (
    validate_appointment_payload,
    AppointmentValidationError
)


class AppointmentService:

    @staticmethod
    def create_appointment(
        db: Session,
        company_id: int,
        employee_id: int,
        payload: dict,
        performed_by: int
    ):
        """
        Appointment creation workflow:
        1. Validate payload
        2. Insert appointment history
        3. Update employee master
        4. Insert audit log
        5. Commit transaction
        """

        try:
            # ---- STEP 1: Validate payload ----
            parsed_dates = validate_appointment_payload(payload)

            employment = payload["employment_details"]
            salary = payload["salary_details"]
            payroll_config = payload["payroll_config"]
            statutory = payload["statutory_details"]
            payroll_flags = payload["payroll_flags"]

            dates = {
                "date_of_birth": parsed_dates["date_of_birth"],
                "date_of_joining": parsed_dates["date_of_joining"],
                "appointment_effective_from": parsed_dates["appointment_effective_from"]
            }

            # ---- STEP 2: Create appointment history ----
            appointment = AppointmentForm(
                company_id=company_id,
                employee_id=employee_id,

                department_id=employment.get("department_id"),
                department_snapshot=employment.get("department_name_snapshot"),

                designation_id=employment.get("designation_id"),
                designation_snapshot=employment.get("designation_snapshot"),

                employment_mode=employment.get("employment_mode"),
                grade_type=employment.get("grade_type"),
                is_grade_pay_applicable=employment.get("is_grade_pay_applicable"),

                basic_amount=salary.get("basic_amount"),
                ctc_amount=salary.get("ctc_amount"),
                salary_mode=salary.get("salary_mode"),

                pay_commission=payroll_config.get("pay_commission"),

                is_pf_applicable=statutory.get("is_pf_applicable"),
                pf_number=statutory.get("pf_number"),
                is_esi_applicable=statutory.get("is_esi_applicable"),
                esi_number=statutory.get("esi_number"),
                is_government_employee=statutory.get("is_government_employee"),

                is_da_applicable=payroll_flags.get("is_da_applicable"),
                is_hra_applicable=payroll_flags.get("is_hra_applicable"),
                is_transport_applicable=payroll_flags.get("is_transport_applicable"),
                is_medical_applicable=payroll_flags.get("is_medical_applicable"),
                is_exgratia_applicable=payroll_flags.get("is_exgratia_applicable"),

                is_pf_deduction_applicable=payroll_flags.get("is_pf_deduction_applicable"),
                is_esi_deduction_applicable=payroll_flags.get("is_esi_deduction_applicable"),
                is_gratuity_applicable=payroll_flags.get("is_gratuity_applicable"),

                date_of_birth=dates["date_of_birth"],
                date_of_joining=dates["date_of_joining"],
                effective_from=dates["appointment_effective_from"],

                created_by=performed_by
            )

            db.add(appointment)
            db.flush()  # ensures appointment_id is available

            # ---- STEP 3: Update Employee Master ----
            employee = db.query(EmployeeMaster).filter(
                EmployeeMaster.employee_id == employee_id,
                EmployeeMaster.company_id == company_id,
                EmployeeMaster.is_active.is_(True)
            ).one_or_none()

            if not employee:
                raise ValueError("Active employee record not found")

            employee.department_id = employment.get("department_id")
            employee.department_name = employment.get("department_name_snapshot")

            employee.designation_id = employment.get("designation_id")
            employee.designation_name = employment.get("designation_snapshot")

            employee.employment_mode = employment.get("employment_mode")
            employee.grade_type = employment.get("grade_type")
            employee.is_grade_pay_applicable = employment.get("is_grade_pay_applicable")

            employee.basic_amount = salary.get("basic_amount")
            employee.ctc_amount = salary.get("ctc_amount")
            employee.salary_mode = salary.get("salary_mode")

            employee.pay_commission = payroll_config.get("pay_commission")

            employee.is_pf_applicable = statutory.get("is_pf_applicable")
            employee.pf_number = statutory.get("pf_number")
            employee.is_esi_applicable = statutory.get("is_esi_applicable")
            employee.esi_number = statutory.get("esi_number")
            employee.is_government_employee = statutory.get("is_government_employee")

            employee.is_da_applicable = payroll_flags.get("is_da_applicable")
            employee.is_hra_applicable = payroll_flags.get("is_hra_applicable")
            employee.is_transport_applicable = payroll_flags.get("is_transport_applicable")
            employee.is_medical_applicable = payroll_flags.get("is_medical_applicable")
            employee.is_exgratia_applicable = payroll_flags.get("is_exgratia_applicable")

            employee.is_pf_deduction_applicable = payroll_flags.get("is_pf_deduction_applicable")
            employee.is_esi_deduction_applicable = payroll_flags.get("is_esi_deduction_applicable")
            employee.is_gratuity_applicable = payroll_flags.get("is_gratuity_applicable")

            employee.date_of_birth = dates["date_of_birth"]
            employee.date_of_joining = dates["date_of_joining"]
            employee.appointment_effective_from = dates["appointment_effective_from"]

            # ---- STEP 4: Audit Log ----
            audit = AuditLog(
                company_id=company_id,
                entity_type="APPOINTMENT",
                entity_id=appointment.appointment_id,
                action="CREATE",
                performed_by=performed_by,
                remarks="New employee appointment created"
            )

            db.add(audit)

            # ---- STEP 5: Commit transaction ----
            db.commit()

            return appointment

        except Exception:
            db.rollback()
            raise
