from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.schema import User, get_db
from app.core.security import get_current_user_id

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("/")
def get_leaderboard(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Top players ranked by reputation — the Criminal Underworld Leaderboard."""
    top_users = db.query(User).order_by(User.reputation.desc()).limit(limit).all()

    return [
        {
            "rank": i + 1,
            "username": u.username,
            "reputation": u.reputation,
            "player_rank": u.rank,
            "missions_completed": u.missions_completed,
            "avatar": u.avatar,
        }
        for i, u in enumerate(top_users)
    ]


@router.get("/me")
def get_my_rank(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """Get current user's leaderboard position."""
    user = db.query(User).filter(User.id == user_id).first()
    rank_position = db.query(func.count(User.id)).filter(
        User.reputation > user.reputation
    ).scalar() + 1

    return {
        "rank": rank_position,
        "username": user.username,
        "reputation": user.reputation,
        "player_rank": user.rank,
        "missions_completed": user.missions_completed,
    }
