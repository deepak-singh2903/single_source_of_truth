from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    Numeric,
    Enum,
    DateTime,
    UniqueConstraint
)

from app.database import Base


class Payroll(Base):
    __tablename__ = "payrolls"

    payroll_id = Column(BigInteger, primary_key=True, autoincrement=True)

    company_id = Column(BigInteger, nullable=False)
    employee_id = Column(BigInteger, nullable=False)

    payroll_year = Column(Integer, nullable=False)
    payroll_month = Column(Integer, nullable=False)

    paid_days = Column(Numeric(5, 2), nullable=False)

    basic_salary = Column(Numeric(12, 2), nullable=False)
    ctc_salary = Column(Numeric(12, 2), nullable=False)

    gross_salary = Column(Numeric(12, 2), nullable=False)
    total_deductions = Column(Numeric(12, 2), nullable=False)
    net_salary = Column(Numeric(12, 2), nullable=False)

    payroll_status = Column(
        Enum("DRAFT", "GENERATED", "LOCKED", name="payroll_status_enum"),
        nullable=False
    )

    generated_at = Column(DateTime)
    locked_at = Column(DateTime)

    created_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "employee_id",
            "payroll_year",
            "payroll_month",
            name="uq_employee_month_payroll"
        ),
    )
