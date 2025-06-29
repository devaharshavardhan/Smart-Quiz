# ──────────────────────────
# Smart Quiz FastAPI Main
# ──────────────────────────

import os
import json
import logging
import time
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError

# ──────────────────────────
# Logging Configuration (define FIRST!)
# ──────────────────────────
logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(message)s", level=logging.INFO)
logger = logging.getLogger("SmartQuizAPI")

# ──────────────────────────
# Load Configuration — wrapped safely
# ──────────────────────────
def load_config() -> dict:
    HERE = os.path.dirname(__file__)
    candidates = [
        "/config.json",
        os.path.join(HERE, "config.json"),
        os.path.abspath(os.path.join(HERE, "..", "config.json")),
    ]
    for cfg_path in candidates:
        if os.path.isfile(cfg_path):
            logger.info(f"Using config: {cfg_path}")
            with open(cfg_path, "r", encoding="utf-8") as f:
                return json.load(f)

    logger.error(f"config.json not found in {candidates}")
    raise RuntimeError("Missing config.json")


raw_cfg = load_config()


class AppConfig(BaseModel):
    generator_mode: str
    model_supported_goals: List[str]
    retrieval_supported_goals: List[str]
    supported_difficulties: List[str]
    default_num_questions: int = Field(5, ge=1)
    max_questions: int = Field(10, ge=1)


config = AppConfig(**raw_cfg)

if config.generator_mode not in ("model", "retrieval"):
    logger.error("Invalid generator_mode in config: %s", config.generator_mode)
    raise RuntimeError("generator_mode must be 'model' or 'retrieval'")

# ──────────────────────────
# Request/Response Schemas
# ──────────────────────────
class MCQRequest(BaseModel):
    goal: str
    difficulty: str
    num_questions: int = Field(config.default_num_questions, gt=0)


class QuestionItem(BaseModel):
    type: str
    question: str
    answer: str
    difficulty: str
    topic: str
    options: Optional[List[str]] = None

    class Config:
        exclude_none = True


class QuizResponse(BaseModel):
    goal: str
    difficulty: str
    questions: List[QuestionItem]

# ──────────────────────────
# FastAPI App Setup
# ──────────────────────────
app = FastAPI(title="🧠 Smart Quiz Generator API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Request validation failed: %s", exc)
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.get("/", tags=["Health"])
def health_check():
    return {"message": "✅ Smart Quiz Generator is running!"}


@app.middleware("http")
async def add_timing_header(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}s"
    return response

# ──────────────────────────
# Utilities
# ──────────────────────────
def clamp_num(n: int) -> int:
    if n <= 0:
        logger.error("Invalid num_questions: %d", n)
        raise HTTPException(400, detail="num_questions must be ≥ 1")
    return min(n, config.max_questions)

# ──────────────────────────
# Quiz Generation Endpoint
# ──────────────────────────
if config.generator_mode == "model":
    from app.model_quiz.entrypoint import run_quiz as run_model_quiz

    @app.post("/generate", response_model=QuizResponse, response_model_exclude_none=True, tags=["Quiz"])
    def generate_model(request: MCQRequest):
        if request.goal not in config.model_supported_goals:
            raise HTTPException(400, detail=f"Unsupported goal: {request.goal}")
        if request.difficulty not in config.supported_difficulties:
            raise HTTPException(400, detail=f"Unsupported difficulty: {request.difficulty}")

        n = clamp_num(request.num_questions)
        logger.info("[Model] Generating %d questions for %s/%s", n, request.goal, request.difficulty)

        try:
            result = run_model_quiz(request.goal, request.difficulty, n)
            items = [QuestionItem(**q) for q in result.get("questions", [])]
            return QuizResponse(goal=result.get("goal"), difficulty=result.get("difficulty"), questions=items)
        except (ValueError, RuntimeError, ValidationError) as e:
            logger.error("Model generation failed: %s", e)
            raise HTTPException(500, detail=str(e))
else:
    from app.retrieval_quiz.entrypoint import retrieve_quiz as run_retrieval_quiz

    @app.post("/generate", response_model=QuizResponse, response_model_exclude_none=True, tags=["Quiz"])
    def generate_retrieval(request: MCQRequest):
        if request.goal not in config.retrieval_supported_goals:
            raise HTTPException(400, detail=f"Unsupported goal: {request.goal}")
        if request.difficulty not in config.supported_difficulties:
            raise HTTPException(400, detail=f"Unsupported difficulty: {request.difficulty}")

        n = clamp_num(request.num_questions)
        logger.info("[Retrieval] Generating %d questions for %s/%s", n, request.goal, request.difficulty)

        try:
            result = run_retrieval_quiz(request.goal, request.difficulty, n)
            items = [QuestionItem(**q) for q in result]
            return QuizResponse(goal=request.goal, difficulty=request.difficulty, questions=items)
        except (ValueError, RuntimeError, ValidationError) as e:
            logger.error("Retrieval generation failed: %s", e)
            raise HTTPException(500, detail=str(e))

# ──────────────────────────
# Entry Point
# ──────────────────────────
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
