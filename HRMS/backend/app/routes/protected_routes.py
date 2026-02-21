from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


protected_bp = Blueprint(
    "protected",
    __name__,
    url_prefix="/protected"
)


# ========================================
# VERIFY CURRENT AUTHENTICATED USER
# ========================================
@protected_bp.route("/me", methods=["GET"])
@jwt_required()
def protected_me():
    """
    Returns current authenticated user details from JWT.
    Used for session validation / frontend auth check.
    """

    try:
        user_id = get_jwt_identity()
        claims = get_jwt()

        return jsonify({
            "message": "JWT is valid",
            "user": {
                "user_id": user_id,
                "company_id": claims.get("company_id"),
                "role_id": claims.get("role_id")
            }
        }), 200

    except Exception as exc:
        print("🔥 PROTECTED ROUTE ERROR:", exc)
        return jsonify({
            "error": "Unauthorized"
        }), 401
