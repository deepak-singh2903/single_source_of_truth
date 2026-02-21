from app.database import get_db
from app.models.user import User

def create_admin():
    with get_db() as db:
        existing = db.query(User).filter(
            User.email == "admin@example.com"
        ).first()

        if existing:
            print("User already exists")
            return

        user = User(
            company_id=1,
            role_id=1,
            email="admin@example.com",
            employee_code=None,
            login_type="EMAIL",
            is_active=True
        )

        user.set_password("Admin@123")

        db.add(user)
        db.commit()

        print("Admin user created successfully")

if __name__ == "__main__":
    create_admin()
