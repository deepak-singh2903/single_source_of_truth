print("🔥 main.py loaded")

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config import Config
from app.database import engine
from app.models.base import Base

# Import all models (very important for metadata)
import app.models  # noqa: F401

# Import blueprints
from app.routes.auth_routes import auth_bp
from app.routes.protected_routes import protected_bp
from app.routes.test_secure_routes import test_secure_bp
from app.routes.appointment_routes import appointment_bp
from app.routes.promotion_routes import promotion_bp
from app.routes.salary_revision_routes import salary_bp
from app.routes.payroll_routes import payroll_bp
from app.routes.payroll_allowance_routes import allowance_bp
from app.routes.pay_commission_routes import pay_commission_bp
from app.routes.employee_routes import employee_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # Initialize JWT
    JWTManager(app)

    # Register blueprints (ONLY ONCE EACH)
    print("➡️ registering blueprints")
    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp)
    app.register_blueprint(test_secure_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(promotion_bp)
    app.register_blueprint(salary_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(allowance_bp)
    app.register_blueprint(pay_commission_bp)
    app.register_blueprint(employee_bp)

    @app.route("/")
    def health_check():
        return {"status": "HRMS backend is running"}, 200

    return app


# Create tables
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
