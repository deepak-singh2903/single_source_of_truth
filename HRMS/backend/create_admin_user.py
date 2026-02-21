from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.utils.security import hash_password

def create_admin_user():
    db = SessionLocal()

    try:
        # Fetch ADMIN role
        admin_role = db.query(Role).filter(Role.role_code == "ADMIN").first()
        if not admin_role:
            print("❌ ADMIN role not found")
            return

        # Check if admin already exists
        existing_user = db.query(User).filter(User.email == "admin@example.com").first()
        if existing_user:
            print("ℹ️ Admin user already exists")
            return

        admin_user = User(
            company_id=1,
            role_id=admin_role.role_id,
            email="admin@example.com",
            employee_code=None,
            login_type="EMAIL",
            password_hash=hash_password("Admin@123"),
            is_active=True
        )

        db.add(admin_user)
        db.commit()

        print("✅ Admin user created successfully")
        print("Login credentials:")
        print("Email: admin@example.com")
        print("Password: Admin@123")

    except Exception as e:
        db.rollback()
        print("❌ Error creating admin user:", e)
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
