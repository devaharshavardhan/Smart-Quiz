from app.retrieval_quiz.quiz_retrieval import QuizGenerator
from app.retrieval_quiz.retrieval_config import CONFIG, DATA_DIR, RETRIEVAL_GOALS, logger

generator = QuizGenerator(CONFIG, DATA_DIR, RETRIEVAL_GOALS, logger)

def retrieve_quiz(goal: str, difficulty: str, num_questions: int):
    return generator.retrieve_quiz(goal, difficulty, num_questions)

if __name__ == "__main__":
    import pprint
    pprint.pprint(retrieve_quiz("Cyber Security", "beginner", 5))