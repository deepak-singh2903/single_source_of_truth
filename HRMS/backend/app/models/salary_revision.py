from datetime import datetime
from sqlalchemy import Column, BigInteger, Numeric, Date, String, DateTime

from app.database import Base


class SalaryRevision(Base):
    __tablename__ = "salary_revisions"

    salary_revision_id = Column(BigInteger, primary_key=True, autoincrement=True)

    company_id = Column(BigInteger, nullable=False)
    employee_id = Column(BigInteger, nullable=False)

    old_basic = Column(Numeric(12, 2), nullable=False)
    old_ctc = Column(Numeric(12, 2), nullable=False)

    new_basic = Column(Numeric(12, 2), nullable=False)
    new_ctc = Column(Numeric(12, 2), nullable=False)

    effective_from_date = Column(Date, nullable=False)

    remarks = Column(String(255))
    created_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
