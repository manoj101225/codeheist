from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.schema import District, UserProgress, get_db
from app.core.security import get_current_user_id

router = APIRouter(prefix="/api/districts", tags=["districts"])


@router.get("/")
def get_all_districts(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    districts = db.query(District).order_by(District.order).all()
    unlocked_ids = {
        p.district_id
        for p in db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.is_unlocked == True,
        ).all()
    }

    result = []
    for d in districts:
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.district_id == d.id,
        ).first()

        result.append({
            "id": d.id,
            "name": d.name,
            "slug": d.slug,
            "description": d.description,
            "topic": d.topic,
            "order": d.order,
            "color": d.color,
            "icon": d.icon,
            "x": d.x,
            "y": d.y,
            "is_unlocked": d.id in unlocked_ids,
            "missions_completed": progress.missions_completed if progress else 0,
            "total_missions": len(d.missions),
        })

    return result


@router.get("/{district_id}")
def get_district(
    district_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    district = db.query(District).filter(District.id == district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")

    # Check if unlocked
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.district_id == district_id,
    ).first()

    is_unlocked = progress.is_unlocked if progress else False

    missions = []
    for m in district.missions:
        missions.append({
            "id": m.id,
            "title": m.title,
            "subtitle": m.subtitle,
            "difficulty": m.difficulty,
            "order": m.order,
            "reputation_reward": m.reputation_reward,
        })

    return {
        "id": district.id,
        "name": district.name,
        "slug": district.slug,
        "description": district.description,
        "topic": district.topic,
        "color": district.color,
        "icon": district.icon,
        "is_unlocked": is_unlocked,
        "missions": missions,
    }
