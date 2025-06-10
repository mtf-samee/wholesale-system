from sqlalchemy import text
from app.database import engine, Base
from app import models  # to register models

print("Creating tables...")

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database(), current_user;"))
    for row in result:
        print(f"Connected to database: {row[0]}, as user: {row[1]}")

Base.metadata.create_all(bind=engine)
print("Tables created!")
