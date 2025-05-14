from fastapi import APIRouter
from .schema import UserCreate, UserLogin
from .crud import create_user, login_user
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.database import get_db

router = APIRouter(prefix="/api")

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user)
