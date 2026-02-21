from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(allowed_roles):
    """
    allowed_roles = list of role_id integers
    Example: @role_required([1, 2])
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role_id = claims.get("role_id")

            if role_id not in allowed_roles:
                return jsonify({
                    "error": "Access forbidden",
                    "required_roles": allowed_roles
                }), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator
