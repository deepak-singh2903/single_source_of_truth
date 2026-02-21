from datetime import date
from sqlalchemy.orm import Session

from app.models.pay_commission_policy import PayCommissionPolicy


class PayCommissionService:
    """
    Handles Pay Commission (CPC) + DA% policies.

    READ by Payroll Engine
    WRITE by Admin / HR

    Fully versioned.
    Past payrolls are never affected.
    """

    # ======================================================
    # PAYROLL ENGINE — GET ACTIVE POLICY FOR DATE
    # ======================================================
    @staticmethod
    def get_active_policy_as_of_date(
        db: Session,
        pay_commission: str,
        as_of_date: date
    ):
        return (
            db.query(PayCommissionPolicy)
            .filter(
                PayCommissionPolicy.pay_commission == pay_commission,
                PayCommissionPolicy.is_active.is_(True),
                PayCommissionPolicy.effective_from <= as_of_date,
                (
                    (PayCommissionPolicy.effective_to.is_(None)) |
                    (PayCommissionPolicy.effective_to >= as_of_date)
                )
            )
            .order_by(PayCommissionPolicy.effective_from.desc())
            .first()
        )

    # ======================================================
    # PAYROLL ENGINE — GET DA %
    # ======================================================
    @staticmethod
    def get_da_percent(
        db: Session,
        pay_commission: str,
        as_of_date: date
    ) -> float:
        policy = PayCommissionService.get_active_policy_as_of_date(
            db=db,
            pay_commission=pay_commission,
            as_of_date=as_of_date
        )

        if not policy:
            return 0.0

        return float(policy.da_percent)

    # ======================================================
    # ADMIN / HR — LIST ALL POLICIES
    # ======================================================
    @staticmethod
    def list_all_policies(db: Session):
        return (
            db.query(PayCommissionPolicy)
            .order_by(PayCommissionPolicy.pay_commission.asc())
            .all()
        )

    # ======================================================
    # ADMIN / HR — UPDATE DA % (VERSIONED)
    # ======================================================
    @staticmethod
    def update_da_percent(
        db: Session,
        company_id: int,
        policy_id: int,
        new_da_percent: float,
        effective_from: date
    ):
        old_policy = (
            db.query(PayCommissionPolicy)
            .filter(
                PayCommissionPolicy.policy_id == policy_id,
                PayCommissionPolicy.company_id == company_id
            )
            .one_or_none()
        )

        if not old_policy:
            raise ValueError("Pay Commission policy not found")

        # Close old policy
        old_policy.effective_to = effective_from
        old_policy.is_active = False

        # ✅ Create new version WITH company_id
        new_policy = PayCommissionPolicy(
            company_id=old_policy.company_id,
            pay_commission=old_policy.pay_commission,
            da_percent=new_da_percent,
            effective_from=effective_from,
            is_active=True
        )

        db.add(new_policy)
        db.commit()

        return new_policy.policy_id

    # ======================================================
    # ADMIN / HR — ACTIVATE / DEACTIVATE CPC
    # ======================================================
    @staticmethod
    def set_policy_status(
        db: Session,
        policy_id: int,
        is_active: bool
    ):
        policy = (
            db.query(PayCommissionPolicy)
            .filter(PayCommissionPolicy.policy_id == policy_id)
            .one_or_none()
        )

        if not policy:
            raise ValueError("Pay Commission policy not found")

        policy.is_active = is_active
        db.commit()

        return policy.policy_id
