from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app import models, schemas
from app.database import SessionLocal
from app.utils import verify_password, create_access_token
from app.config import SECRET_KEY, ALGORITHM
from app.models import UserRole

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Token scheme for protecting routes (for Swagger UI compatibility)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Login route
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Get current user from token
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Get active user
async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    # Optional: Add logic to check if user is active
    return current_user

# Admin or staff only
async def get_current_active_admin_or_staff(current_user: models.User = Depends(get_current_active_user)):
    if current_user.role not in [UserRole.admin, UserRole.staff]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user
