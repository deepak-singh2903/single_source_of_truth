from sqlalchemy import Column, BigInteger, String, Enum, JSON, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(BigInteger, primary_key=True, autoincrement=True)
    company_id = Column(BigInteger, nullable=False)

    entity_type = Column(String(100), nullable=False)
    entity_id = Column(BigInteger, nullable=False)

    action_type = Column(
        Enum("CREATE","UPDATE","STATUS_CHANGE","EXIT", name="audit_action_enum"),
        nullable=False
    )

    old_value = Column(JSON)
    new_value = Column(JSON)

    performed_by = Column(BigInteger, nullable=False)
    performed_at = Column(TIMESTAMP, server_default=func.now())
