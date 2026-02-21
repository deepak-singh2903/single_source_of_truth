from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from app.database import get_db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    login_value = data.get("login")   # email OR employee_code
    password = data.get("password")

    if not login_value or not password:
        return jsonify({"message": "Login and password required"}), 400

    with get_db() as db:

        # Try EMAIL login
        user = db.query(User).filter(
            User.email == login_value,
            User.login_type == "EMAIL",
            User.is_active == True
        ).first()

        # If not found, try EMP_CODE login
        if not user:
            user = db.query(User).filter(
                User.employee_code == login_value,
                User.login_type == "EMP_CODE",
                User.is_active == True
            ).first()

        if not user or not user.verify_password(password):
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(
            identity=str(user.user_id),
            additional_claims={
                "company_id": user.company_id,
                "role_id": user.role_id
            }
        )

        refresh_token = create_refresh_token(
            identity=str(user.user_id)
        )

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()

    new_access_token = create_access_token(identity=user_id)

    return jsonify({"access_token": new_access_token}), 200
