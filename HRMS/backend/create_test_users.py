from app.database import get_db
from app.models.user import User

users = [
    {"email": "admin@test.com", "role_id": 1},
    {"email": "hr@test.com", "role_id": 2},
    {"email": "finance@test.com", "role_id": 3},
    {"email": "employee@test.com", "role_id": 4},
]

def create_users():
    with get_db() as db:
        for u in users:
            existing = db.query(User).filter(
                User.email == u["email"]
            ).first()

            if existing:
                print(f"{u['email']} already exists")
                continue

            user = User(
                company_id=1,
                role_id=u["role_id"],
                email=u["email"],
                employee_code=None,
                login_type="EMAIL",
                is_active=True
            )

            user.set_password("Test@123")

            db.add(user)

        db.commit()

    print("Test users created successfully")

if __name__ == "__main__":
    create_users()
