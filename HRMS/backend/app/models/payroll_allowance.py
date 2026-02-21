from sqlalchemy import Column, BigInteger, String, Enum, Numeric, Boolean
from app.database import Base


class PayrollAllowance(Base):
    __tablename__ = "payroll_allowances"

    allowance_id = Column(BigInteger, primary_key=True, autoincrement=True)

    company_id = Column(BigInteger, nullable=False)
    allowance_code = Column(String(50), nullable=False)

    is_applicable = Column(Boolean, default=True)

    calculation_type = Column(
        Enum("PERCENTAGE", "FIXED", name="allowance_calc_type"),
        nullable=False
    )

    calculation_value = Column(Numeric(10, 2), nullable=False)
