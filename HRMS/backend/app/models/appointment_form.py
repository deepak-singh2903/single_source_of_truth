from sqlalchemy import Column, BigInteger, String, Boolean, Date, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base

class AppointmentForm(Base):
    __tablename__ = "appointment_forms"

    appointment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, nullable=False)
    employee_id = Column(BigInteger, nullable=False)

    grade_type = Column(Enum("GRADE","NON_GRADE", name="grade_type_enum"), nullable=False)
    is_grade_pay_applicable = Column(Boolean, default=False)

    current_basic = Column(DECIMAL(12,2), nullable=False)
    current_ctc = Column(DECIMAL(12,2), nullable=False)

    salary_mode = Column(Enum("BANK","CHEQUE", name="salary_mode_enum"), nullable=False)
    bank_name = Column(String(255))
    bank_account_number = Column(String(50))
    ifsc_code = Column(String(20))

    is_government_account = Column(Boolean, default=False)
    is_pf_applicable = Column(Boolean, default=False)
    is_esi_applicable = Column(Boolean, default=False)

    pf_number = Column(String(50))
    uan_number = Column(String(50))
    esi_number = Column(String(50))

    is_da_applicable = Column(Boolean, default=False)
    is_hra_applicable = Column(Boolean, default=False)
    is_transport_applicable = Column(Boolean, default=False)
    is_medical_applicable = Column(Boolean, default=False)
    is_exgratia_applicable = Column(Boolean, default=False)

    is_pf_deduction_applicable = Column(Boolean, default=False)
    is_esi_deduction_applicable = Column(Boolean, default=False)
    is_gratuity_applicable = Column(Boolean, default=False)

    effective_from_date = Column(Date, nullable=False)
    remarks = Column(String(255))

    created_by = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
