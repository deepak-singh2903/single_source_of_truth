from datetime import datetime, date
import calendar
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.payroll import Payroll
from app.models.employee_master import EmployeeMaster
from app.services.salary_revision_service import SalaryRevisionService
from app.services.pay_commission_service import PayCommissionService


# ======================================================
# SIMPLE SALARY UTIL FUNCTIONS
# ======================================================

def calculate_pf(basic, da, pf_scheme_type):
    total = basic + da

    if pf_scheme_type == "NO":
        return 0

    if pf_scheme_type == "YES WITH NEW SCHEME":
        if basic < 15000:
            return round(total * 0.12)
        else:
            return 1800

    if pf_scheme_type == "YES WITH OLD SCHEME":
        return round(total * 0.12)

    return 0


def calculate_hra(basic, hra_type, hra_percentage):
    if hra_type == "NO":
        return 0

    if hra_type == "PERCENTAGE":
        if hra_percentage is None:
            return 0
        return round(basic * float(hra_percentage) / 100)

    if hra_type == "FIXED":
        return round(basic / 2)

    return 0


# ======================================================
# PAYROLL SERVICE
# ======================================================

class PayrollService:

    # ======================================================
    # PAID DAYS ENTRY
    # ======================================================
    @staticmethod
    def upsert_paid_days(
        db: Session,
        company_id: int,
        payroll_year: int,
        payroll_month: int,
        employee_id: int,
        paid_days,
        performed_by: int
    ):
        employee = db.query(EmployeeMaster).filter(
            EmployeeMaster.company_id == company_id,
            EmployeeMaster.employee_id == employee_id,
            EmployeeMaster.is_active.is_(True)
        ).one_or_none()

        if not employee:
            raise ValueError("Active employee not found")

        payroll = db.query(Payroll).filter(
            Payroll.company_id == company_id,
            Payroll.employee_id == employee_id,
            Payroll.payroll_year == payroll_year,
            Payroll.payroll_month == payroll_month
        ).one_or_none()

        if payroll:
            if payroll.payroll_status == "LOCKED":
                raise ValueError("Payroll is locked for this month")
            payroll.paid_days = paid_days
        else:
            payroll = Payroll(
                company_id=company_id,
                employee_id=employee_id,
                payroll_year=payroll_year,
                payroll_month=payroll_month,
                paid_days=paid_days,
                basic_salary=0,
                ctc_salary=0,
                gross_salary=0,
                total_deductions=0,
                net_salary=0,
                payroll_status="DRAFT",
                created_by=performed_by,
                created_at=datetime.utcnow()
            )
            db.add(payroll)

        db.commit()
        return payroll.payroll_id

    # ======================================================
    # GENERATE PAYROLL (SHEET ALIGNED ENGINE)
    # ======================================================
    @staticmethod
    def generate_payroll(
        db: Session,
        company_id: int,
        employee_id: int,
        payroll_year: int,
        payroll_month: int,
        performed_by: int
    ):

        payroll = db.query(Payroll).filter(
            Payroll.company_id == company_id,
            Payroll.employee_id == employee_id,
            Payroll.payroll_year == payroll_year,
            Payroll.payroll_month == payroll_month
        ).one_or_none()

        if not payroll:
            raise ValueError("Payroll record not found")

        if payroll.payroll_status == "LOCKED":
            raise ValueError("Payroll is locked")

        if payroll.paid_days is None:
            raise ValueError("Paid days not entered")

        # --------------------------------------------------
        # Calendar
        # --------------------------------------------------
        total_days = calendar.monthrange(payroll_year, payroll_month)[1]
        month_end_date = date(payroll_year, payroll_month, total_days)

        # --------------------------------------------------
        # Salary (Revision Snapshot)
        # --------------------------------------------------
        salary = SalaryRevisionService.get_effective_salary_as_of_date(
            db=db,
            company_id=company_id,
            employee_id=employee_id,
            as_of_date=month_end_date
        )

        monthly_basic = Decimal(salary["basic"])
        monthly_ctc = Decimal(salary["ctc"])

        # --------------------------------------------------
        # Prorate Basic & CTC
        # --------------------------------------------------
        per_day_basic = monthly_basic / Decimal(total_days)
        per_day_ctc = monthly_ctc / Decimal(total_days)

        earned_basic = per_day_basic * Decimal(payroll.paid_days)
        earned_ctc = per_day_ctc * Decimal(payroll.paid_days)

        if earned_ctc <= 0:
            earned_ctc = Decimal("0.00")

        # --------------------------------------------------
        # Employee Snapshot
        # --------------------------------------------------
        employee = db.query(EmployeeMaster).filter(
            EmployeeMaster.employee_id == employee_id
        ).one()

        # --------------------------------------------------
        # DA
        # --------------------------------------------------
        earned_da = Decimal("0.00")

        if employee.is_da_applicable and employee.pay_commission_type != "NOT APPLICABLE":
            da_percent = PayCommissionService.get_da_percent(
                db=db,
                pay_commission=employee.pay_commission_type,
                as_of_date=month_end_date
            )
            earned_da = (Decimal(da_percent) / Decimal("100")) * earned_basic

        # --------------------------------------------------
        # HRA
        # --------------------------------------------------
        earned_hra = Decimal("0.00")

        if employee.hra_type != "NO":
            earned_hra = Decimal(
                calculate_hra(
                    float(earned_basic),
                    employee.hra_type,
                    float(employee.hra_percentage) if employee.hra_percentage else 0
                )
            )

        # --------------------------------------------------
        # Transport (Fixed Full Month)
        # --------------------------------------------------
        transport_amount = Decimal("0.00")

        if employee.is_transport_applicable:
            da_percent = PayCommissionService.get_da_percent(
                db=db,
                pay_commission=employee.pay_commission_type,
                as_of_date=month_end_date
            )

            base_transport = Decimal("3600")
            transport_amount = base_transport + (
                base_transport * Decimal(da_percent) / Decimal("100")
            )

        # --------------------------------------------------
        # Medical (Fixed Full Month)
        # --------------------------------------------------
        medical_amount = Decimal("75") if employee.is_medical_applicable else Decimal("0.00")

        # --------------------------------------------------
        # PF
        # --------------------------------------------------
        pf_amount = Decimal("0.00")

        if employee.is_pf_applicable and employee.is_pf_deduction_applicable:
            pf_amount = Decimal(
                calculate_pf(
                    float(earned_basic),
                    float(earned_da),
                    employee.pf_scheme_type
                )
            )

        # --------------------------------------------------
        # Gratuity
        # --------------------------------------------------
        gratuity_amount = Decimal("0.00")

        if employee.is_gratuity_applicable:
            gratuity_amount = (
                (earned_basic + earned_da)
                * Decimal("4.807")
                / Decimal("100")
            )

        # --------------------------------------------------
        # Ex-Gratia (Balancing)
        # --------------------------------------------------
        exgratia_amount = (
            earned_ctc
            - (
                earned_basic
                + earned_da
                + earned_hra
                + transport_amount
                + medical_amount
                + pf_amount
                + gratuity_amount
            )
        )

        if exgratia_amount < 0:
            exgratia_amount = Decimal("0.00")

        # --------------------------------------------------
        # Gross & Net
        # --------------------------------------------------
        gross_salary = (
            earned_basic
            + earned_da
            + earned_hra
            + transport_amount
            + medical_amount
            + exgratia_amount
        )

        total_deductions = pf_amount
        net_salary = gross_salary - total_deductions

        # --------------------------------------------------
        # Snapshot Save
        # --------------------------------------------------
        payroll.basic_salary = round(earned_basic)
        payroll.ctc_salary = round(earned_ctc)
        payroll.gross_salary = round(gross_salary)
        payroll.total_deductions = round(total_deductions)
        payroll.net_salary = round(net_salary)

        payroll.payroll_status = "GENERATED"
        payroll.generated_at = datetime.utcnow()

        db.commit()
        return payroll.payroll_id

    # ======================================================
    # PAYROLL BREAKUP (READ SNAPSHOT)
    # ======================================================
    @staticmethod
    def get_payroll_breakup(
        db: Session,
        company_id: int,
        employee_id: int,
        payroll_year: int,
        payroll_month: int
    ):
        payroll = db.query(Payroll).filter(
            Payroll.company_id == company_id,
            Payroll.employee_id == employee_id,
            Payroll.payroll_year == payroll_year,
            Payroll.payroll_month == payroll_month
        ).one_or_none()

        if not payroll:
            raise ValueError("Payroll record not found")

        return {
            "employee_id": employee_id,
            "company_id": company_id,
            "period": {
                "year": payroll_year,
                "month": payroll_month
            },
            "earnings": {
                "basic_salary": payroll.basic_salary,
                "gross_salary": payroll.gross_salary
            },
            "deductions": {
                "total_deductions": payroll.total_deductions
            },
            "net_salary": payroll.net_salary,
            "status": payroll.payroll_status
        }

    # ======================================================
    # LOCK PAYROLL
    # ======================================================
    @staticmethod
    def lock_payroll(
        db: Session,
        company_id: int,
        employee_id: int,
        payroll_year: int,
        payroll_month: int,
        performed_by: int
    ):
        payroll = db.query(Payroll).filter(
            Payroll.company_id == company_id,
            Payroll.employee_id == employee_id,
            Payroll.payroll_year == payroll_year,
            Payroll.payroll_month == payroll_month
        ).one_or_none()

        if not payroll:
            raise ValueError("Payroll record not found")

        if payroll.payroll_status == "LOCKED":
            return payroll.payroll_id

        if payroll.payroll_status != "GENERATED":
            raise ValueError("Payroll must be GENERATED before locking")

        payroll.payroll_status = "LOCKED"
        payroll.locked_at = datetime.utcnow()

        db.commit()
        return payroll.payroll_id
