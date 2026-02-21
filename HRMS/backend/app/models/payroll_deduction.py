from sqlalchemy import Column, BigInteger, String, Enum, Boolean, DECIMAL
from app.database import Base


class PayrollDeduction(Base):
    __tablename__ = "payroll_deductions"

    deduction_id = Column(BigInteger, primary_key=True)
    company_id = Column(BigInteger, nullable=False)

    deduction_code = Column(String(50), nullable=False)
    deduction_name = Column(String(100), nullable=False)

    calculation_type = Column(
        Enum("PERCENTAGE", "FIXED", "NONE", name="deduction_calculation_type_enum"),
        nullable=False
    )
    calculation_value = Column(DECIMAL(10, 2))

    is_employee_deduction = Column(Boolean, default=True)
    is_employer_deduction = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)
