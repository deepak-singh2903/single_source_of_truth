from sqlalchemy.orm import Session
from app.models.payroll_allowance import PayrollAllowance


class PayrollAllowanceService:

    @staticmethod
    def get_company_allowances(db: Session, company_id: int):
        return db.query(PayrollAllowance).filter(
            PayrollAllowance.company_id == company_id,
            PayrollAllowance.is_applicable.is_(True)
        ).all()

    @staticmethod
    def upsert_allowance(
        db: Session,
        company_id: int,
        allowance_code: str,
        calculation_type: str,
        calculation_value
    ):
        allowance = db.query(PayrollAllowance).filter(
            PayrollAllowance.company_id == company_id,
            PayrollAllowance.allowance_code == allowance_code
        ).one_or_none()

        if allowance:
            allowance.calculation_type = calculation_type
            allowance.calculation_value = calculation_value
            allowance.is_applicable = True
        else:
            allowance = PayrollAllowance(
                company_id=company_id,
                allowance_code=allowance_code,
                calculation_type=calculation_type,
                calculation_value=calculation_value,
                is_applicable=True
            )
            db.add(allowance)

        db.commit()
        return allowance.allowance_id
