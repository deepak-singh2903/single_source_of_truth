from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.models.base import Base


class PromotionForm(Base):
    __tablename__ = "promotion_forms"

    promotion_id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employee_master.employee_id"), nullable=False)

    # ---- New (after promotion) ----
    new_department_id = Column(Integer, nullable=True)
    new_department_snapshot = Column(String(100), nullable=True)

    new_designation_id = Column(Integer, nullable=False)
    new_designation_snapshot = Column(String(100), nullable=False)

    new_grade_type = Column(String(20), nullable=True)
    is_grade_pay_applicable = Column(Boolean, default=False)

    # ---- Meta ----
    effective_date = Column(Date, nullable=False)
    remarks = Column(Text, nullable=True)

    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
