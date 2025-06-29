from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import os
import json
class QuestionMatcher:
    def __init__(self, config, data_dir, retrieval_goals, logger):
        self.bank = []
        for goal, filename in config.get("domain_files", {}).items():
            if goal.lower() not in retrieval_goals:
                continue

            path = os.path.join(data_dir, filename)
            if not os.path.isfile(path):
                logger.warning(f"Missing file for goal '{goal}': {path}")
                continue

            try:
                with open(path, "r", encoding="utf-8") as f:
                    questions = json.load(f)
                self.bank.extend(questions)
                logger.info(f"Loaded {len(questions)} questions for '{goal}'")
            except Exception as e:
                logger.error(f"Failed to load {path}: {e}")

        if not self.bank:
            raise RuntimeError("No questions loaded. Check domain_files & data directory.")

        texts = [
            (q.get("context", "") + " " + q.get("question", "")).strip()
            for q in self.bank
        ]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)

        self.meta = [
            {
                "topic": q.get("topic", "").lower(),
                "goal": q.get("goal", "").lower(),
                "type": q.get("type", ""),
                "difficulty": q.get("difficulty", "")
            }
            for q in self.bank
        ]

    def match(self, topics, goal, max_q=5, difficulty=None, q_types=None):
        query = " ".join(topics)
        vec = self.vectorizer.transform([query])
        scores = cosine_similarity(vec, self.matrix).flatten()

        for i, m in enumerate(self.meta):
            if any(t in m["topic"] or m["topic"] in t for t in topics):
                scores[i] += 0.2

        top_k_idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:50]
        random.shuffle(top_k_idxs)

        selected = []
        for i in top_k_idxs:
            md = self.meta[i]
            if md["goal"].lower() != goal.lower():
                continue
            if difficulty and md["difficulty"].lower() != difficulty.lower():
                continue
            if q_types and md["type"].lower() not in [t.lower() for t in q_types]:
                continue

            q = dict(self.bank[i])
            q["score"] = float(scores[i])
            selected.append(q)
            if len(selected) >= max_q:
                return selected

        logger.warning(f"[{goal}] Only {len(selected)} questions matched. Using fallback.")

        additional = [
            q for i, q in enumerate(self.bank)
            if q.get("goal", "").lower() == goal.lower()
            and q.get("difficulty", "").lower() == difficulty.lower()
            and (not q_types or q.get("type", "").lower() in [t.lower() for t in q_types])
            and q not in selected
        ]
        random.shuffle(additional)
        selected.extend(additional[: max_q - len(selected)])

        return selected
