from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # identity is now ONLY user_id (string)
            user_id = get_jwt_identity()
            claims = get_jwt()

            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401

            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "error": "Forbidden",
                    "required_roles": allowed_roles,
                    "your_role": user_role
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def admin_only(fn):
    return role_required("ADMIN")(fn)


def hr_only(fn):
    return role_required("HR")(fn)


def employee_only(fn):
    return role_required("EMPLOYEE")(fn)


def company_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        claims = get_jwt()

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        token_company_id = claims.get("company_id")
        route_company_id = kwargs.get("company_id")

        if route_company_id is None:
            return jsonify({"error": "company_id missing in route"}), 400

        if token_company_id != route_company_id:
            return jsonify({
                "error": "Forbidden - cross company access denied",
                "your_company_id": token_company_id,
                "requested_company_id": route_company_id
            }), 403

        return fn(*args, **kwargs)
    return wrapper
