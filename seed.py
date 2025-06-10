from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db: Session = SessionLocal()

admin_email = "admin@example.com"

existing_user = db.query(User).filter(User.email == admin_email).first()

if not existing_user:
    admin_user = User(
        email=admin_email,
        hashed_password=pwd_context.hash("admin123"),
        full_name="Admin User",
        role="admin"
    )
    db.add(admin_user)
    db.commit()
    print("Admin user created.")
else:
    print("Admin user already exists.")
