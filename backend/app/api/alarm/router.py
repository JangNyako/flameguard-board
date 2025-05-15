from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.detection_log import DetectionLog

router = APIRouter()

@router.get("/api/alarm/list")
def get_alarm_list(db: Session = Depends(get_db)):
    logs = db.query(DetectionLog).order_by(DetectionLog.created_at.desc()).all()
    return [
        {
            "message": log.message,
            "created_at": log.created_at.strftime("%Y-%m-%d %H:%M"),
            "result_image": log.result_image
        }
        for log in logs
    ]

@router.get("/api/alarm/latest")
def get_latest_alarms(db: Session = Depends(get_db)):
    logs = (
        db.query(DetectionLog)
        .filter(DetectionLog.message != "safe")
        .order_by(DetectionLog.created_at.desc())
        .limit(3)
        .all()
    )
    return [
        {
            "message": log.message,
            "created_at": log.created_at.strftime("%Y-%m-%d %H:%M"),
            "result_image": log.result_image
        }
        for log in logs
    ]
