from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import authenticate_user, hash_password
from app.models.database import get_db
from app.models.models import User

router = APIRouter()

# User login endpoint
@router.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect user or password")
    return {"access_token": user.email, "token_type": "bearer"}

# User registration
@router.post("/registrer")
def registrer_user(email:str, password: str, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = hash_password(password)
        new_user = User(email=email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500)