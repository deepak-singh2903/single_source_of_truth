from sqlalchemy import Column, BigInteger, Boolean, Date, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.models.base import Base


class TransportPolicy(Base):
    __tablename__ = "transport_policy"

    policy_id = Column(BigInteger, primary_key=True, autoincrement=True)

    base_amount = Column(DECIMAL(10, 2), default=0)

    calculation_type = Column(
        Enum("FIXED", "PERCENTAGE", name="transport_policy_type_enum"),
        nullable=True
    )

    is_active = Column(Boolean, default= False)

    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
