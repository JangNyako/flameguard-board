from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base

class Board(Base):
    __tablename__ = "board"

    board_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    user_name = Column(String, nullable=False)  # <- 이름 저장
    created_at = Column(DateTime, nullable=False)
    img = Column(String, nullable=True)