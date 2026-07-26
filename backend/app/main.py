"""
CodeHeist — GTA5-Themed DSA Learning Platform
Main application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.schema import init_db, SessionLocal, District, Mission, TestCase
from app.api import auth, districts, missions, submissions, progress, leaderboard
from app.seed.syllabus_data import DISTRICTS, MISSIONS

app = FastAPI(
    title="CodeHeist API",
    description="GTA5-Themed DSA Learning Platform — Every heist is a coding challenge",
    version="1.0.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(auth.router)
app.include_router(districts.router)
app.include_router(missions.router)
app.include_router(submissions.router)
app.include_router(progress.router)
app.include_router(leaderboard.router)


@app.on_event("startup")
def startup():
    """Initialize database and seed data on startup."""
    init_db()
    seed_data()


def seed_data():
    """Seed districts and missions if they don't exist yet."""
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(District).count() > 0:
            return

        # Seed districts
        district_map = {}
        for d_data in DISTRICTS:
            district = District(
                name=d_data["name"],
                slug=d_data["slug"],
                description=d_data["description"],
                topic=d_data["topic"],
                order=d_data["order"],
                color=d_data["color"],
                icon=d_data["icon"],
                x=d_data["x"],
                y=d_data["y"],
                unlock_requirement=d_data["unlock_requirement"],
            )
            db.add(district)
            db.flush()
            district_map[d_data["slug"]] = district.id

        # Seed missions
        for district_slug, mission_list in MISSIONS.items():
            district_id = district_map.get(district_slug)
            if not district_id:
                continue

            for m_data in mission_list:
                mission = Mission(
                    district_id=district_id,
                    title=m_data["title"],
                    subtitle=m_data["subtitle"],
                    description=m_data["description"],
                    difficulty=m_data["difficulty"],
                    order=m_data["order"],
                    reputation_reward=m_data["reputation_reward"],
                    starter_python=m_data.get("starter_python", ""),
                    starter_cpp=m_data.get("starter_cpp", ""),
                    starter_java=m_data.get("starter_java", ""),
                    starter_js=m_data.get("starter_js", ""),
                    hint_1=m_data.get("hint_1", ""),
                    hint_2=m_data.get("hint_2", ""),
                )
                db.add(mission)
                db.flush()

                # Seed test cases
                for tc_data in m_data.get("test_cases", []):
                    tc = TestCase(
                        mission_id=mission.id,
                        order=m_data["test_cases"].index(tc_data),
                        input_data=tc_data["input"],
                        expected_output=tc_data["expected"],
                        is_hidden=tc_data.get("is_hidden", False),
                    )
                    db.add(tc)

        db.commit()
        print(f"[OK] Seeded {len(DISTRICTS)} districts and {sum(len(v) for v in MISSIONS.values())} missions")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seed error: {e}")
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "name": "CodeHeist API",
        "version": "1.0.0",
        "status": "operational",
        "message": "Welcome to the underworld. Every heist is a coding challenge.",
    }
