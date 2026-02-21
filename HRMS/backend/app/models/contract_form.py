from sqlalchemy import Column, BigInteger, String, Date, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base

class ContractForm(Base):
    __tablename__ = "contract_forms"

    contract_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, nullable=False)
    employee_id = Column(BigInteger, nullable=False)

    contract_start_date = Column(Date, nullable=False)
    contract_end_date = Column(Date, nullable=False)
    remarks = Column(String(255))

    created_by = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
