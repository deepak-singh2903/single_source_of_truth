from datetime import datetime
from sqlalchemy.orm import Session

from app.models.employee_master import EmployeeMaster
from app.models.promotion_form import PromotionForm
from app.models.audit_log import AuditLog


DATE_FORMAT = "%d-%b-%Y"  # DD-MMM-YYYY


class PromotionService:

    # =========================
    # APPLY PROMOTION (P5.1)
    # =========================
    @staticmethod
    def apply_promotion(
        db: Session,
        company_id: int,
        employee_id: int,
        payload: dict,
        performed_by: int
    ):
        try:
            promotion = payload.get("promotion_details")
            effective_date_str = payload.get("effective_date")

            if not promotion:
                raise ValueError("promotion_details is required")

            if not effective_date_str:
                raise ValueError("effective_date is required")

            try:
                effective_date = datetime.strptime(
                    effective_date_str, DATE_FORMAT
                ).date()
            except Exception:
                raise ValueError("Invalid effective_date format. Expected DD-MMM-YYYY")

            if not promotion.get("new_designation_id"):
                raise ValueError("new_designation_id is mandatory")

            remarks = payload.get("remarks")

            # --- Insert promotion history ---
            promotion_record = PromotionForm(
                company_id=company_id,
                employee_id=employee_id,

                department_id=promotion.get("new_department_id"),
                department_name_snapshot=promotion.get("new_department_snapshot"),

                designation_id=promotion.get("new_designation_id"),
                designation_snapshot=promotion.get("new_designation_snapshot"),

                employment_mode=promotion.get("employment_mode"),

                effective_from_date=effective_date,
                remarks=remarks,
                created_by=performed_by
            )

            db.add(promotion_record)
            db.flush()  # get promotion_id

            # --- Update Employee Master ---
            employee = db.query(EmployeeMaster).filter(
                EmployeeMaster.employee_id == employee_id,
                EmployeeMaster.company_id == company_id,
                EmployeeMaster.is_active.is_(True)
            ).one_or_none()

            if not employee:
                raise ValueError("Active employee record not found")

            if promotion.get("new_department_id"):
                employee.department_id = promotion.get("new_department_id")
                employee.department_name = promotion.get("new_department_snapshot")

            employee.designation_id = promotion.get("new_designation_id")
            employee.designation_name = promotion.get("new_designation_snapshot")

            if promotion.get("employment_mode"):
                employee.employment_mode = promotion.get("employment_mode")

            # --- Audit log ---
            audit = AuditLog(
                company_id=company_id,
                entity_type="PROMOTION",
                entity_id=promotion_record.promotion_id,
                action_type="CREATE",
                old_value=None,
                new_value={
                    "department_id": promotion.get("new_department_id"),
                    "designation_id": promotion.get("new_designation_id"),
                    "employment_mode": promotion.get("employment_mode"),
                    "effective_date": effective_date_str,
                    "remarks": remarks
                },
                performed_by=performed_by
            )

            db.add(audit)
            db.commit()

            return promotion_record.promotion_id

        except Exception:
            db.rollback()
            raise

    # =========================
    # PROMOTION HISTORY (P5.2)
    # =========================
    @staticmethod
    def get_promotion_history(
        db: Session,
        company_id: int,
        employee_id: int
    ):
        records = db.query(PromotionForm).filter(
            PromotionForm.company_id == company_id,
            PromotionForm.employee_id == employee_id
        ).order_by(
            PromotionForm.effective_date.desc()
        ).all()

        history = []
        for r in records:
            history.append({
                "promotion_id": r.promotion_id,

                "new_department_id": r.new_department_id,
                "new_department_snapshot": r.new_department_snapshot,

                "new_designation_id": r.new_designation_id,
                "new_designation_snapshot": r.new_designation_snapshot,

                "effective_date": r.effective_date.isoformat(),

                "remarks": r.remarks,
                "created_at": r.created_at.isoformat()
            })


        return history
