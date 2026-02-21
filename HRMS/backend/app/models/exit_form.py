from sqlalchemy import Column, BigInteger, String, Date, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base

class ExitForm(Base):
    __tablename__ = "exit_forms"

    exit_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, nullable=False)
    employee_id = Column(BigInteger, nullable=False)

    exit_type = Column(
        Enum("RESIGNATION","TERMINATION","ABSCONDED", name="exit_type_enum"),
        nullable=False
    )

    resignation_date = Column(Date, nullable=False)
    last_working_date = Column(Date, nullable=False)

    reason = Column(String(255))
    remarks = Column(String(255))

    created_by = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
