from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.schema import User, UserProgress, Attempt, District, get_db
from app.core.security import get_current_user_id

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("/me")
def get_my_progress(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    user = db.query(User).filter(User.id == user_id).first()
    progress_records = db.query(UserProgress).filter(
        UserProgress.user_id == user_id
    ).all()

    districts_progress = []
    for p in progress_records:
        district = db.query(District).filter(District.id == p.district_id).first()
        if district:
            districts_progress.append({
                "district_id": district.id,
                "district_name": district.name,
                "topic": district.topic,
                "missions_completed": p.missions_completed,
                "total_missions": len(district.missions),
                "is_unlocked": p.is_unlocked,
            })

    # Recent attempts
    recent = db.query(Attempt).filter(
        Attempt.user_id == user_id
    ).order_by(Attempt.submitted_at.desc()).limit(10).all()

    recent_attempts = [
        {
            "mission_id": a.mission_id,
            "language": a.language,
            "status": a.status,
            "tests_passed": a.tests_passed,
            "tests_total": a.tests_total,
            "execution_time_ms": a.execution_time_ms,
            "submitted_at": a.submitted_at.isoformat(),
        }
        for a in recent
    ]

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "rank": user.rank,
            "reputation": user.reputation,
            "missions_completed": user.missions_completed,
            "avatar": user.avatar,
        },
        "districts": districts_progress,
        "recent_attempts": recent_attempts,
    }
