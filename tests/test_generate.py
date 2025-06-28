import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_GOAL = "AWS Cloud Practitioner"
VALID_DIFFICULTY = "beginner"
DEFAULT_NUM = 5
MAX_NUM = 10
SUPPORTED_TYPES = {"mcq", "short_answer"}

# ────────────────────────────────
# 1. Test core structure & count
# ────────────────────────────────

@pytest.mark.parametrize("num_q", [1, DEFAULT_NUM, MAX_NUM])
def test_generate_correct_structure_and_count(num_q):
    payload = {
        "goal": VALID_GOAL,
        "difficulty": VALID_DIFFICULTY,
        "num_questions": num_q
    }
    start = time.time()
    response = client.post("/generate", json=payload)
    elapsed = time.time() - start

    assert response.status_code == 200, response.text
    data = response.json()

    # Structure
    assert data.get("goal") == VALID_GOAL
    assert data.get("difficulty") == VALID_DIFFICULTY
    assert isinstance(data.get("questions"), list)

    # Count
    assert 0 < len(data["questions"]) <= num_q

    # Field checks
    for q in data["questions"]:
        assert q.get("type") in SUPPORTED_TYPES
        assert isinstance(q.get("question"), str) and q["question"].strip()
        assert isinstance(q.get("answer"), str) and q["answer"].strip()
        if q["type"] == "mcq":
            opts = q.get("options")
            assert isinstance(opts, list)
            assert len(opts) >= 2
            assert all(isinstance(opt, str) for opt in opts)

    # ⏱️ Performance check (warn only)
    if num_q == DEFAULT_NUM:
        if elapsed > 1.5:
            pytest.warns(None, f"⚠️ Response took {elapsed:.2f}s (expected < 1.5s)")

# ────────────────────────────────
# 2. Invalid num_questions → 422
# ────────────────────────────────

@pytest.mark.parametrize("num_q", [0, -1])
def test_invalid_num_questions_returns_422(num_q):
    payload = {
        "goal": VALID_GOAL,
        "difficulty": VALID_DIFFICULTY,
        "num_questions": num_q
    }
    r = client.post("/generate", json=payload)
    assert r.status_code == 422

# ────────────────────────────────
# 3. Invalid goal / difficulty → 400
# ────────────────────────────────

def test_invalid_goal_returns_400():
    payload = {
        "goal": "NotAGoal",
        "difficulty": VALID_DIFFICULTY,
        "num_questions": 3
    }
    r = client.post("/generate", json=payload)
    assert r.status_code == 400

def test_invalid_difficulty_returns_400():
    payload = {
        "goal": VALID_GOAL,
        "difficulty": "hardest",
        "num_questions": 3
    }
    r = client.post("/generate", json=payload)
    assert r.status_code == 400

# ────────────────────────────────
# 4. Missing fields → 422
# ────────────────────────────────

@pytest.mark.parametrize("payload", [
    {"difficulty": VALID_DIFFICULTY, "num_questions": DEFAULT_NUM},  # missing goal
    {"goal": VALID_GOAL, "num_questions": DEFAULT_NUM},              # missing difficulty
])
def test_missing_fields_returns_422(payload):
    r = client.post("/generate", json=payload)
    assert r.status_code == 422
