from sqlalchemy import Column, BigInteger, String, Boolean, Date, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base


class PFPolicy(Base):
    __tablename__ = "pf_policy"

    policy_id = Column(BigInteger, primary_key=True, autoincrement=True)

    scheme_name = Column(String(50), nullable=False)
    employee_percent = Column(DECIMAL(5, 2), nullable=False)
    employer_percent = Column(DECIMAL(5, 2), nullable=False)
    additional_percent = Column(DECIMAL(5, 2), default=0)

    wage_ceiling = Column(DECIMAL(10, 2), default=15000)

    deduct_employer_share = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
