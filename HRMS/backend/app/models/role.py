from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_code = Column(String(50), unique=True, nullable=False)
    role_name = Column(String(100), nullable=False)
    description = Column(String(255))

    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<Role {self.role_code}>"
