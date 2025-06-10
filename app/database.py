from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get the DATABASE_URL from .env
DATABASE_URL = "postgresql://postgres:202023@localhost:5432/wholesale_db"

# Create engine (connect to the database)
engine = create_engine(DATABASE_URL)

# Create session class to interact with DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models (tables)
Base = declarative_base()
