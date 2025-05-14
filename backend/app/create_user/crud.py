from app.db.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException

def create_user(db: Session, user_data):
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, login_data):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
