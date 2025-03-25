from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.models import User
from app.schemas.users import UserRead
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme -> login via username & password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# function to hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# fucntion to authenticate user
def authenticate_user(db: Session, email: str, password:str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    return user

# Dependency to get current user
def get_current_user(db: Session = Depends(get_db), token = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.email == token).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    return user