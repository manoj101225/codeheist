from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timezone

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ──────────────────────────── User ────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    avatar = Column(String(20), default="gangster_1")
    rank = Column(String(30), default="Street Punk")
    reputation = Column(Integer, default=0)
    missions_completed = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    attempts = relationship("Attempt", back_populates="user")
    progress = relationship("UserProgress", back_populates="user")


# ──────────────────────────── District ────────────────────────────
class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(60), unique=True, nullable=False, index=True)
    description = Column(Text)
    topic = Column(String(60), nullable=False)  # e.g. "Arrays", "Binary Search"
    order = Column(Integer, nullable=False)  # District unlock order
    color = Column(String(20), default="#ff0040")  # Neon color for map
    icon = Column(String(30), default="🏙️")
    x = Column(Float, default=0.0)  # Map position X
    y = Column(Float, default=0.0)  # Map position Y
    unlock_requirement = Column(Integer, default=0)  # Missions needed from previous district

    missions = relationship("Mission", back_populates="district", order_by="Mission.order")


# ──────────────────────────── Mission ────────────────────────────
class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    title = Column(String(150), nullable=False)  # GTA-themed heist name
    subtitle = Column(String(150))  # Real DSA problem name
    description = Column(Text, nullable=False)  # Full problem statement
    difficulty = Column(String(10), nullable=False)  # Easy / Medium / Hard
    order = Column(Integer, nullable=False)
    reputation_reward = Column(Integer, default=100)

    # Starter code templates per language (JSON strings)
    starter_python = Column(Text, default="")
    starter_cpp = Column(Text, default="")
    starter_java = Column(Text, default="")
    starter_js = Column(Text, default="")

    # Hints
    hint_1 = Column(Text, default="")
    hint_2 = Column(Text, default="")

    district = relationship("District", back_populates="missions")
    test_cases = relationship("TestCase", back_populates="mission", order_by="TestCase.order")
    attempts = relationship("Attempt", back_populates="mission")


# ──────────────────────────── TestCase ────────────────────────────
class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    order = Column(Integer, default=0)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False)  # Hidden test cases not shown to user

    mission = relationship("Mission", back_populates="test_cases")


# ──────────────────────────── Attempt ────────────────────────────
class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    language = Column(String(15), nullable=False)  # python, cpp, java, javascript
    code = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)  # passed, failed, error, timeout
    tests_passed = Column(Integer, default=0)
    tests_total = Column(Integer, default=0)
    execution_time_ms = Column(Float, default=0.0)
    error_message = Column(Text, default="")
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="attempts")
    mission = relationship("Mission", back_populates="attempts")


# ──────────────────────────── UserProgress ────────────────────────────
class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    missions_completed = Column(Integer, default=0)
    is_unlocked = Column(Boolean, default=False)
    best_time_ms = Column(Float, default=0.0)

    user = relationship("User", back_populates="progress")


# ──────────────────────────── BanditModelState ────────────────────────────
class BanditModelState(Base):
    __tablename__ = "bandit_model_state"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    # JSON string of topic weights: {"arrays": 0.5, "binary_search": 0.3, ...}
    topic_weights = Column(Text, default="{}")
    total_pulls = Column(Integer, default=0)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    Base.metadata.create_all(bind=engine)
