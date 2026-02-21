from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    Date,
    Text,
    Enum,
    DECIMAL,
    TIMESTAMP
)
from sqlalchemy.sql import func
from app.models.base import Base


class EmployeeMaster(Base):
    __tablename__ = "employee_master"

    employee_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, nullable=False)
    company_code = Column(String(50), nullable=False)
    employee_code = Column(String(50), nullable=False)

    # Personal Details
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=True)

    gender = Column(
        Enum("MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY", name="gender_enum"),
        nullable=False
    )

    date_of_birth = Column(Date, nullable=False)

    guardian_relation_prefix = Column(
        Enum("S/O", "D/O", "W/O", "NA", name="guardian_relation_enum"),
        nullable=False
    )
    guardian_name = Column(String(255), nullable=False)

    mobile_number = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)

    # Employment Snapshot
    date_of_joining = Column(Date, nullable=False)

    department_id = Column(BigInteger, nullable=False)
    department_name_snapshot = Column(String(255), nullable=False)

    designation_id = Column(BigInteger)
    designation_snapshot = Column(String(255), nullable=False)

    employment_status = Column(
        Enum("ACTIVE", "ON_HOLD", "INACTIVE", "EXITED", name="employment_status_enum"),
        nullable=False
    )

    employment_mode = Column(
        Enum(
            "PROBATION",
            "CONFIRMED",
            "CONTRACT",
            "TEMPORARY",
            "INTERN",
            "CONSULTANT",
            name="employment_mode_enum",
        ),
        nullable=False
    )

    # Statutory & Identity
    aadhar_number = Column(String(20), nullable=False)
    pan_number = Column(String(20), nullable=False)

    salary_mode = Column(
        Enum("BANK", "CHEQUE", name="salary_mode_enum"),
        nullable=False
    )

    bank_name = Column(String(255))
    bank_account_number = Column(String(50))
    ifsc_code = Column(String(20))
    is_government_account = Column(Boolean, default=False)

    pf_scheme_type = Column(
        Enum(
            "YES WITH OLD SCHEME",
            "YES WITH NEW SCHEME",
            "NO",
            name="pf_scheme_type_enum"
        ),
        nullable=False
    )

    is_pf_applicable = Column(Boolean, default=False)
    is_esi_applicable = Column(Boolean, default=False)

    pf_number = Column(String(50))
    uan_number = Column(String(50))
    esi_number = Column(String(50))

    # Payroll Inputs & Flags
    grade_type = Column(
        Enum("GRADE", "NON GRADE", name="grade_type_enum"),
        nullable=False
    )

    pay_commission_type = Column(
        Enum(
            "6 CPC",
            "7 CPC",
            "8 CPC",
            "9 CPC",
            "10 CPC",
            "NOT APPLICABLE",
            name="pay_commission_type_enum"
        ),
        nullable=False
    )


    hra_type = Column(
        Enum(
            "PERCENTAGE",
            "FIXED",
            "NO",
            name="hra_type_enum"
        ),
        nullable=False
    )

    hra_percentage = Column(DECIMAL(5,2), nullable=True)


    is_grade_pay_applicable = Column(Boolean, default=False)

    current_basic = Column(DECIMAL(12, 2), nullable=False)
    current_ctc = Column(DECIMAL(12, 2), nullable=False)

    is_da_applicable = Column(Boolean, default=False)
    is_transport_applicable = Column(Boolean, default=False)
    is_medical_applicable = Column(Boolean, default=False)
    is_exgratia_applicable = Column(Boolean, default=False)

    is_pf_deduction_applicable = Column(Boolean, default=False)
    is_esi_deduction_applicable = Column(Boolean, default=False)
    is_gratuity_applicable = Column(Boolean, default=False)

    # System Fields
    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<EmployeeMaster {self.employee_code}>"
