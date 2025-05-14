# router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.share_crud import get_user_by_email
from pydantic import BaseModel

router = APIRouter(prefix="/api")

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=data.email)
    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다.")
    return {"user_id": user.user_id, "name": user.name, "role": user.role}
