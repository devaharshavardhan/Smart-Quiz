import os
import json
import logging

logger = logging.getLogger("model.config")

ROOT = os.getenv("PROJECT_ROOT", os.getcwd())
CONFIG_PATH = os.path.join(ROOT, "config.json")

if not os.path.isfile(CONFIG_PATH):
    logger.error("Missing config.json. App cannot start.")
    raise RuntimeError("Missing config.json. App cannot start.")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

SUPPORTED_GOALS = set(cfg["model_supported_goals"])
SUPPORTED_DIFFICULTIES = set(cfg["supported_difficulties"])
DEFAULT_NUM_QUESTIONS = cfg["default_num_questions"]
MAX_NUM_QUESTIONS = cfg["max_questions"]
INPUT_PATH = cfg["model_dataset"]
T5_MODEL_PATH = cfg["t5-model_path"]
GRAMMAR_MODEL_PATH = cfg["grammar_model_path"]
QA_MODEL_PATHS = cfg["qa_model_paths"]
SBERT_PATH = cfg["sentence_transformer_path"]
USE_QA = True
QG_TEMPLATE = "generate question: domain: {goal} context: {context} answer: {answer}"
T5_GEN_CONFIG = {
    "max_length": 32,
    "num_beams": 3,
    "do_sample": False,
    "early_stopping": True,
    "num_return_sequences": 1
}
