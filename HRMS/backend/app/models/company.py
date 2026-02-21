from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_code = Column(String(50), unique=True, nullable=False)
    company_name = Column(String(255), nullable=False)
    official_email_domain = Column(String(255), nullable=False)

    # ==========================
    # Payroll Policy Flags
    # ==========================
    deduct_employer_pf_from_employee = Column(Boolean, default=False)
    deduct_employer_esi_from_employee = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<Company {self.company_code}>"
