from sqlalchemy import Column, BigInteger, String, Boolean, Date, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base

class GradeBasicChangeForm(Base):
    __tablename__ = "grade_basic_change_forms"

    change_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, nullable=False)
    employee_id = Column(BigInteger, nullable=False)

    grade_type = Column(Enum("GRADE","NON_GRADE", name="grade_type_enum"), nullable=False)
    is_grade_pay_applicable = Column(Boolean, default=False)
    new_basic = Column(DECIMAL(12,2), nullable=False)

    effective_from_date = Column(Date, nullable=False)
    reason = Column(String(255))

    created_by = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
