import os
import json
import logging

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Check multiple candidate locations
CANDIDATE_PATHS = [
    "/config.json",  # Docker mount path
    os.path.abspath(os.path.join(APP_DIR, "..", "..", "config.json")),  # root of project
    os.path.abspath(os.path.join(APP_DIR, "..", "config.json")),        # fallback (inside app)
]

for path in CANDIDATE_PATHS:
    if os.path.isfile(path):
        CONFIG_PATH = path
        break
else:
    raise RuntimeError(f"❌ Missing config.json in: {CANDIDATE_PATHS}")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# Load constants
DATA_DIR = os.path.join(os.path.dirname(CONFIG_PATH), "data")
RETRIEVAL_GOALS = {g.lower() for g in CONFIG.get("retrieval_supported_goals", [])}

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("retrieval_quiz_model")
