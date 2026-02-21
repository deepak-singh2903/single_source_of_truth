from sqlalchemy import Column, BigInteger, String, Date, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base

class StatusChangeForm(Base):
    __tablename__ = "status_change_forms"

    status_change_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, nullable=False)
    employee_id = Column(BigInteger, nullable=False)

    employment_status = Column(
        Enum("ACTIVE","ON_HOLD","INACTIVE","EXITED", name="employment_status_enum"),
        nullable=False
    )

    effective_from_date = Column(Date, nullable=False)
    reason = Column(String(255))
    remarks = Column(String(255))

    created_by = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
