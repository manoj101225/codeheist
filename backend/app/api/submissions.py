from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.models.schema import Mission, TestCase, Attempt, User, UserProgress, District, get_db
from app.core.security import get_current_user_id
from app.core.judge import judge_submission
from app.services.bandit import update_bandit
from app.core.config import REPUTATION_REWARDS, MISSIONS_TO_UNLOCK

router = APIRouter(prefix="/api/submissions", tags=["submissions"])


class SubmitRequest(BaseModel):
    mission_id: int
    language: str  # python, cpp, java, javascript
    code: str


@router.post("/")
def submit_code(
    req: SubmitRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    # Validate language
    if req.language not in ("python", "cpp", "java", "javascript"):
        raise HTTPException(status_code=400, detail="Unsupported language")

    # Get mission and test cases
    mission = db.query(Mission).filter(Mission.id == req.mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    test_cases = [
        {"input": tc.input_data, "expected": tc.expected_output}
        for tc in mission.test_cases
    ]

    if not test_cases:
        raise HTTPException(status_code=500, detail="No test cases for this mission")

    # Run judge
    verdict = judge_submission(req.code, req.language, test_cases, mission_title=mission.title)

    # Check if user already solved this mission
    already_solved = db.query(Attempt).filter(
        Attempt.user_id == user_id,
        Attempt.mission_id == req.mission_id,
        Attempt.status == "passed",
    ).first()

    # Save attempt
    attempt = Attempt(
        user_id=user_id,
        mission_id=req.mission_id,
        language=req.language,
        code=req.code,
        status=verdict.status,
        tests_passed=verdict.tests_passed,
        tests_total=verdict.tests_total,
        execution_time_ms=verdict.total_time_ms,
        error_message=verdict.error_message,
    )
    db.add(attempt)

    # Update reputation and progress if first solve
    reputation_gained = 0
    district_unlocked = None

    if verdict.status == "passed" and not already_solved:
        reward = REPUTATION_REWARDS.get(mission.difficulty, 100)
        reputation_gained = reward

        user = db.query(User).filter(User.id == user_id).first()
        user.reputation += reward
        user.missions_completed += 1

        # Update rank based on reputation
        user.rank = _calculate_rank(user.reputation)

        # Update district progress
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.district_id == mission.district_id,
        ).first()
        if progress:
            progress.missions_completed += 1

            # Check if next district should be unlocked
            if progress.missions_completed >= MISSIONS_TO_UNLOCK:
                current_district = db.query(District).filter(
                    District.id == mission.district_id
                ).first()
                next_district = db.query(District).filter(
                    District.order == current_district.order + 1
                ).first()

                if next_district:
                    existing = db.query(UserProgress).filter(
                        UserProgress.user_id == user_id,
                        UserProgress.district_id == next_district.id,
                    ).first()
                    if not existing:
                        new_progress = UserProgress(
                            user_id=user_id,
                            district_id=next_district.id,
                            is_unlocked=True,
                        )
                        db.add(new_progress)
                        district_unlocked = {
                            "id": next_district.id,
                            "name": next_district.name,
                            "topic": next_district.topic,
                        }

        # Update bandit model
        district = db.query(District).filter(District.id == mission.district_id).first()
        update_bandit(db, user_id, district.topic, success=True)

    elif verdict.status in ("failed", "error", "timeout"):
        district = db.query(District).filter(District.id == mission.district_id).first()
        update_bandit(db, user_id, district.topic, success=False)

    db.commit()

    # Build test results for response (hide hidden test details)
    test_results = []
    for r in verdict.results:
        test_results.append({
            "test_index": r.test_index,
            "passed": r.passed,
            "input": r.input_data,
            "expected": r.expected,
            "actual": r.actual,
            "execution_time_ms": r.execution_time_ms,
            "error": r.error,
        })

    return {
        "status": verdict.status,
        "tests_passed": verdict.tests_passed,
        "tests_total": verdict.tests_total,
        "total_time_ms": verdict.total_time_ms,
        "error_message": verdict.error_message,
        "test_results": test_results,
        "reputation_gained": reputation_gained,
        "district_unlocked": district_unlocked,
    }


def _calculate_rank(reputation: int) -> str:
    if reputation >= 10000:
        return "Crime Lord"
    elif reputation >= 7500:
        return "Kingpin"
    elif reputation >= 5000:
        return "Boss"
    elif reputation >= 3000:
        return "Lieutenant"
    elif reputation >= 1500:
        return "Enforcer"
    elif reputation >= 750:
        return "Hustler"
    elif reputation >= 300:
        return "Associate"
    elif reputation >= 100:
        return "Runner"
    return "Street Punk"
