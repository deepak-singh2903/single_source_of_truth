from sqlalchemy import Column, BigInteger, String, Boolean, Date, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func

from app.models.base import Base


class PayCommissionPolicy(Base):
    __tablename__ = "pay_commission_policy"

    policy_id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 🔑 COMPANY SCOPING (CRITICAL)
    company_id = Column(BigInteger, nullable=False)

    pay_commission = Column(String(50), nullable=False)
    da_percent = Column(DECIMAL(6, 2), nullable=False, default=0)

    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<PayCommissionPolicy {self.pay_commission} {self.da_percent}%>"
