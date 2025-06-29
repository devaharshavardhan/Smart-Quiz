# app/model_quiz/entrypoint.py

from app.model_quiz.quiz_model import run_model_quiz

# Public interface for FastAPI
def run_quiz(goal: str, difficulty: str, num_questions: int):
    return run_model_quiz(goal, difficulty, num_questions)

# Optional CLI test
if __name__ == "__main__":
    import pprint
    result = run_quiz("Amazon SDE", "beginner", 5)
    pprint.pprint(result)
