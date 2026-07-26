import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database
DATABASE_URL = f"sqlite:///{BASE_DIR / 'codeheist.db'}"

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "codeheist-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Judge Settings
JUDGE_TIMEOUT_MS = {
    "python": 2000,
    "cpp": 2000,
    "java": 3000,
    "javascript": 2000,
}
JUDGE_MEMORY_LIMIT_MB = 256

# Reputation rewards per difficulty
REPUTATION_REWARDS = {
    "Easy": 100,
    "Medium": 250,
    "Hard": 500,
}

# Missions needed to unlock next district
MISSIONS_TO_UNLOCK = 5
