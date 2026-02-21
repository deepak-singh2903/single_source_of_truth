from sqlalchemy.orm import Session
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.models.role import Role
from app.utils.security import verify_password


class AuthService:

    @staticmethod
    def login(db: Session, identifier: str, password: str):
        """
        identifier:
          - email for Admin/HR/Finance/Auditor
          - employee_code for Employee
        """

        # Try email login first
        user = db.query(User).filter(
            User.email == identifier,
            User.is_active == True
        ).first()

        # If not found by email, try employee_code
        if not user:
            user = db.query(User).filter(
                User.employee_code == identifier,
                User.is_active == True
            ).first()

        if not user:
            raise ValueError("Invalid credentials")

        # Verify password
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        # Load role
        role = db.query(Role).filter(Role.role_id == user.role_id).first()
        if not role:
            raise ValueError("User role not found")

        # Enforce login rules
        if role.role_code in ("ADMIN", "HR", "FINANCE", "AUDITOR"):
            if user.login_type != "EMAIL":
                raise ValueError("This role must login using email")

        if role.role_code == "EMPLOYEE":
            if user.login_type != "EMP_CODE":
                raise ValueError("Employee must login using employee code")

        # Create JWT token
        additional_claims = {
            "company_id": user.company_id,
            "role": role.role_code
        }

        access_token = create_access_token(
            identity=str(user.user_id),   # MUST be string
            additional_claims=additional_claims
        )

        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "user": {
                "user_id": user.user_id,
                "role": role.role_code,
                "company_id": user.company_id
            }
        }
