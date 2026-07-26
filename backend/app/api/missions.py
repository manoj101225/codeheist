from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.schema import Mission, TestCase, Attempt, get_db
from app.core.security import get_current_user_id
from app.services.bandit import recommend_next_mission

router = APIRouter(prefix="/api/missions", tags=["missions"])


@router.get("/{mission_id}")
def get_mission(
    mission_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Get visible test cases (non-hidden)
    visible_tests = [
        {"input": tc.input_data, "expected": tc.expected_output}
        for tc in mission.test_cases
        if not tc.is_hidden
    ]

    # Get user's best attempt
    best_attempt = db.query(Attempt).filter(
        Attempt.user_id == user_id,
        Attempt.mission_id == mission_id,
        Attempt.status == "passed",
    ).order_by(Attempt.execution_time_ms).first()

    return {
        "id": mission.id,
        "district_id": mission.district_id,
        "title": mission.title,
        "subtitle": mission.subtitle,
        "description": mission.description,
        "difficulty": mission.difficulty,
        "reputation_reward": mission.reputation_reward,
        "starter_python": mission.starter_python,
        "starter_cpp": mission.starter_cpp,
        "starter_java": mission.starter_java,
        "starter_js": mission.starter_js,
        "hint_1": mission.hint_1,
        "hint_2": mission.hint_2,
        "sample_tests": visible_tests,
        "is_solved": best_attempt is not None,
        "best_time_ms": best_attempt.execution_time_ms if best_attempt else None,
    }


@router.get("/next/recommended")
def get_recommended(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    rec = recommend_next_mission(db, user_id)
    if not rec:
        return {"message": "You've completed all available missions! Legend status."}
    return rec
