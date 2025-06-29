from app.retrieval_quiz.topic_extractor import TopicExtractor
from app.retrieval_quiz.question_matcher import QuestionMatcher
import random
import logging

logger = logging.getLogger(__name__)

class QuizGenerator:
    def __init__(self, config, data_dir, retrieval_goals, logger):
        self.matcher = QuestionMatcher(config, data_dir, retrieval_goals, logger)
        self.extractor = TopicExtractor(config.get("spacy_model", "en_core_web_sm"))

    def retrieve_quiz(self, goal, difficulty, num_questions):
        goal_questions = [
            q for q in self.matcher.bank
            if q.get("goal", "").lower() == goal.lower()
        ]

        if not goal_questions:
            logger.warning(f"No questions found for goal: {goal}")
            return []

        seed = random.choice(goal_questions)
        seed_text = f"{seed.get('context', '')} {seed.get('question', '')}".strip()
        topics = self.extractor.extract(seed_text) or [goal.lower()]

        logger.info(f"[{goal}] Extracted topics: {topics}")

        return self.matcher.match(
            topics=topics,
            goal=goal,
            max_q=num_questions,
            difficulty=difficulty,
            q_types=["mcq", "short_answer"]
        )