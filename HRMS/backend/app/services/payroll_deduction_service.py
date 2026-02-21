from sqlalchemy.orm import Session
from app.models.payroll_deduction import PayrollDeduction


class PayrollDeductionService:

    @staticmethod
    def get_active_deductions(db: Session, company_id: int):
        return db.query(PayrollDeduction).filter(
            PayrollDeduction.company_id == company_id,
            PayrollDeduction.is_active.is_(True)
        ).all()
