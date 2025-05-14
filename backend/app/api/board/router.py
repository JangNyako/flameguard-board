from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.board import Board
from app.db.models.user import User
from datetime import datetime
import os
import shutil
from uuid import uuid4
from app.db.models import board as board_model
from app.db.models import user as user_model

router = APIRouter(prefix="/api/board")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/create")
def create_board(
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    img: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    # 유저 아이디로 유저 조회
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 이미지 저장 처리
    img_url = None
    if img:
        ext = img.filename.split('.')[-1]
        filename = f"{uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

        img_url = f"/static/uploads/{filename}"

    # 게시글 생성
    post = Board(
        title=title,
        content=content,
        user_name=user.name,
        created_at=datetime.utcnow(),
        img=img_url
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {"message": "success"}


@router.get("/list")
def get_boards(db: Session = Depends(get_db)):
    boards = db.query(Board).order_by(Board.created_at.desc()).all()
    return boards

@router.get("/recent")
def get_recent_boards(db: Session = Depends(get_db)):
    recent_boards = (
        db.query(
            Board.board_id,
            Board.title,
            Board.created_at,
            Board.user_name.label("author_name")
        )
        .order_by(Board.created_at.desc())
        .limit(3)
        .all()
    )

    # SQLAlchemy Row 객체를 dict로 바꾸기
    return [
        {
            "board_id": row.board_id,
            "title": row.title,
            "created_at": row.created_at.isoformat(),
            "author_name": row.author_name,
        }
        for row in recent_boards
    ]