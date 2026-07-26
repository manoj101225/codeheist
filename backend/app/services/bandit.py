"""
Multi-Armed Bandit (Thompson Sampling) recommendation engine.
Recommends the next best mission/topic based on user performance history.
"""

import json
import random
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.schema import BanditModelState, District, UserProgress, Attempt, Mission


# Topic slugs matching district topics
ALL_TOPICS = [
    "arrays", "binary_search", "strings", "linked_lists",
    "recursion_backtracking", "bit_manipulation", "stack_queue",
    "sliding_window", "heaps", "greedy", "binary_trees",
    "bst", "graphs", "dynamic_programming",
]


def _get_or_create_state(db: Session, user_id: int) -> BanditModelState:
    state = db.query(BanditModelState).filter(BanditModelState.user_id == user_id).first()
    if not state:
        # Initialize with uniform weights
        initial_weights = {topic: {"alpha": 1.0, "beta": 1.0} for topic in ALL_TOPICS}
        state = BanditModelState(
            user_id=user_id,
            topic_weights=json.dumps(initial_weights),
            total_pulls=0,
        )
        db.add(state)
        db.commit()
        db.refresh(state)
    return state


def update_bandit(db: Session, user_id: int, topic: str, success: bool):
    """
    Update the bandit model after a submission.
    Thompson Sampling: increment alpha on success, beta on failure.
    """
    state = _get_or_create_state(db, user_id)
    weights = json.loads(state.topic_weights)

    topic_key = topic.lower().replace(" ", "_").replace("&", "and")
    if topic_key not in weights:
        weights[topic_key] = {"alpha": 1.0, "beta": 1.0}

    if success:
        weights[topic_key]["alpha"] += 1.0
    else:
        weights[topic_key]["beta"] += 1.0

    state.topic_weights = json.dumps(weights)
    state.total_pulls += 1
    state.last_updated = datetime.now(timezone.utc)
    db.commit()


def recommend_next_mission(db: Session, user_id: int) -> Optional[dict]:
    """
    Use Thompson Sampling to recommend the next mission.
    Prioritizes topics where the user struggles (higher beta = more practice needed).
    """
    state = _get_or_create_state(db, user_id)
    weights = json.loads(state.topic_weights)

    # Get user's unlocked districts
    unlocked = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.is_unlocked == True,
    ).all()
    unlocked_district_ids = {p.district_id for p in unlocked}

    # If no districts unlocked, recommend first district
    if not unlocked_district_ids:
        first_district = db.query(District).filter(District.order == 1).first()
        if first_district:
            first_mission = db.query(Mission).filter(
                Mission.district_id == first_district.id
            ).order_by(Mission.order).first()
            if first_mission:
                return {
                    "mission_id": first_mission.id,
                    "title": first_mission.title,
                    "subtitle": first_mission.subtitle,
                    "district": first_district.name,
                    "difficulty": first_mission.difficulty,
                    "reason": "Start your criminal career here!",
                }
        return None

    # Thompson Sampling: sample from Beta distribution for each topic
    topic_scores = {}
    for topic_key, params in weights.items():
        # Higher beta relative to alpha means user needs more practice
        # We want to recommend topics where user struggles
        score = random.betavariate(params["beta"], params["alpha"])
        topic_scores[topic_key] = score

    # Sort by score descending (highest need for practice first)
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)

    # Find an unsolved mission in the recommended topic
    for topic_key, score in sorted_topics:
        district = db.query(District).filter(
            District.id.in_(unlocked_district_ids)
        ).all()

        for d in district:
            d_topic_key = d.topic.lower().replace(" ", "_").replace("&", "and")
            if d_topic_key != topic_key:
                continue

            # Find first unsolved mission in this district
            solved_mission_ids = {
                a.mission_id for a in db.query(Attempt).filter(
                    Attempt.user_id == user_id,
                    Attempt.status == "passed",
                ).all()
            }

            unsolved = db.query(Mission).filter(
                Mission.district_id == d.id,
                ~Mission.id.in_(solved_mission_ids) if solved_mission_ids else True,
            ).order_by(Mission.order).first()

            if unsolved:
                return {
                    "mission_id": unsolved.id,
                    "title": unsolved.title,
                    "subtitle": unsolved.subtitle,
                    "district": d.name,
                    "difficulty": unsolved.difficulty,
                    "reason": f"Your {d.topic} skills need sharpening — time for more heists!",
                }

    return None
