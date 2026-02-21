from datetime import datetime
from sqlalchemy.orm import Session

from app.models.salary_revision import SalaryRevision
from app.models.employee_master import EmployeeMaster
from app.models.audit_log import AuditLog

DATE_FORMAT = "%d-%b-%Y"  # DD-MMM-YYYY


class SalaryRevisionService:

    # ============================
    # APPLY SALARY REVISION (P6.2)
    # ============================
    @staticmethod
    def apply_salary_revision(
        db: Session,
        company_id: int,
        employee_id: int,
        payload: dict,
        performed_by: int
    ):
        try:
            # ---- STEP 1: Validate payload ----
            effective_date_str = payload.get("effective_from_date")
            new_basic = payload.get("new_basic")
            new_ctc = payload.get("new_ctc")
            remarks = payload.get("remarks")

            if not effective_date_str:
                raise ValueError("effective_from_date is required")

            if new_basic is None or new_ctc is None:
                raise ValueError("new_basic and new_ctc are required")

            try:
                effective_date = datetime.strptime(
                    effective_date_str, DATE_FORMAT
                ).date()
            except Exception:
                raise ValueError(
                    "Invalid effective_from_date format. Expected DD-MMM-YYYY"
                )

            # ---- STEP 2: Fetch active employee ----
            employee = db.query(EmployeeMaster).filter(
                EmployeeMaster.company_id == company_id,
                EmployeeMaster.employee_id == employee_id,
                EmployeeMaster.is_active.is_(True)
            ).one_or_none()

            if not employee:
                raise ValueError("Active employee not found")

            # ---- STEP 3: Insert salary revision history ----
            revision = SalaryRevision(
                company_id=company_id,
                employee_id=employee_id,

                old_basic=employee.current_basic,
                old_ctc=employee.current_ctc,

                new_basic=new_basic,
                new_ctc=new_ctc,

                effective_from_date=effective_date,
                remarks=remarks,

                created_by=performed_by
            )

            db.add(revision)
            db.flush()  # get salary_revision_id

            # ---- STEP 4: Update employee master snapshot ----
            employee.current_basic = new_basic
            employee.current_ctc = new_ctc

            # ---- STEP 5: Audit log ----
            audit = AuditLog(
                company_id=company_id,
                entity_type="SALARY_REVISION",
                entity_id=revision.salary_revision_id,
                action_type="UPDATE",
                old_value={
                    "basic": str(revision.old_basic),
                    "ctc": str(revision.old_ctc)
                },
                new_value={
                    "basic": str(new_basic),
                    "ctc": str(new_ctc),
                    "effective_from_date": effective_date_str
                },
                performed_by=performed_by
            )

            db.add(audit)

            # ---- STEP 6: Commit ----
            db.commit()

            return revision.salary_revision_id

        except Exception:
            db.rollback()
            raise

    # ==================================
    # SALARY REVISION HISTORY (P6.3)
    # ==================================
    @staticmethod
    def get_salary_revision_history(
        db: Session,
        company_id: int,
        employee_id: int
    ):
        records = (
            db.query(SalaryRevision)
            .filter(
                SalaryRevision.company_id == company_id,
                SalaryRevision.employee_id == employee_id
            )
            .order_by(SalaryRevision.effective_from_date.desc())
            .all()
        )

        history = []
        for r in records:
            history.append({
                "salary_revision_id": r.salary_revision_id,

                "old_basic": str(r.old_basic),
                "old_ctc": str(r.old_ctc),

                "new_basic": str(r.new_basic),
                "new_ctc": str(r.new_ctc),

                "effective_from_date": r.effective_from_date.isoformat(),
                "remarks": r.remarks,
                "created_at": r.created_at.isoformat()
            })

        return history


    # ==================================================
    # EFFECTIVE SALARY SELECTION (P6.4)
    # ==================================================
    @staticmethod
    def get_effective_salary_as_of_date(
        db: Session,
        company_id: int,
        employee_id: int,
        as_of_date
    ):
        """
        Returns the salary values applicable as of a given date.
        Used by Payroll & Reports later.
        """

        # 1️⃣ Find latest salary revision effective on or before date
        revision = (
            db.query(SalaryRevision)
            .filter(
                SalaryRevision.company_id == company_id,
                SalaryRevision.employee_id == employee_id,
                SalaryRevision.effective_from_date <= as_of_date
            )
            .order_by(SalaryRevision.effective_from_date.desc())
            .first()
        )

        # 2️⃣ If revision exists → use it
        if revision:
            return {
                "source": "SALARY_REVISION",
                "basic": revision.new_basic,
                "ctc": revision.new_ctc,
                "effective_from_date": revision.effective_from_date
            }

        # 3️⃣ Else fall back to Employee Master snapshot
        employee = db.query(EmployeeMaster).filter(
            EmployeeMaster.company_id == company_id,
            EmployeeMaster.employee_id == employee_id
        ).one_or_none()

        if not employee:
            raise ValueError("Employee not found for salary selection")

        return {
            "source": "EMPLOYEE_MASTER",
            "basic": employee.current_basic,
            "ctc": employee.current_ctc,
            "effective_from_date": None
        }
