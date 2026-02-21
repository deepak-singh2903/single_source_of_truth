from sqlalchemy import Column, BigInteger, String, Date, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base

class ReimbursementForm(Base):
    __tablename__ = "reimbursement_forms"

    reimbursement_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, nullable=False)
    employee_id = Column(BigInteger, nullable=False)

    reimbursement_type = Column(String(100), nullable=False)
    reimbursement_amount = Column(DECIMAL(12,2), nullable=False)
    reimbursement_date = Column(Date, nullable=False)

    supporting_document = Column(String(255))
    remarks = Column(String(255))

    created_by = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
