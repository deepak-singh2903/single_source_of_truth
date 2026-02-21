from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Boolean,
    Enum,
    TIMESTAMP
)
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)

    company_id = Column(BigInteger, nullable=False)
    role_id = Column(Integer, nullable=False)

    email = Column(String(255), nullable=True)
    employee_code = Column(String(50), nullable=True)

    login_type = Column(
        Enum("EMAIL", "EMP_CODE", name="login_type_enum"),
        nullable=False
    )

    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    last_login_at = Column(TIMESTAMP, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<User {self.user_id}>"

    # 🔐 Password Handling
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)
