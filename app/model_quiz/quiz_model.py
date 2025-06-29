import random
import json
from typing import List, Dict, Any
from .loaders_model import load_t5, load_grammar, load_qa, load_sbert
from .data_model import load_dataset, filter_dataset
from sentence_transformers import util

from .config_model import SUPPORTED_GOALS, SUPPORTED_DIFFICULTIES, DEFAULT_NUM_QUESTIONS, MAX_NUM_QUESTIONS, INPUT_PATH, QG_TEMPLATE, T5_GEN_CONFIG, USE_QA

q_tok, q_mdl, q_dev = load_t5()
g_tok, g_mdl = load_grammar()
qa_models = load_qa()
sbert = load_sbert()

def generate_questions(contexts: List[str], answers: List[str], goal: str, types: List[str]) -> List[str]:
    prompts = [QG_TEMPLATE.format(goal=goal, context=c, answer=(c if t == "short_answer" else a)) for c, a, t in zip(contexts, answers, types)]
    inputs = q_tok(prompts, return_tensors="pt", truncation=True, padding=True, max_length=256).to(q_dev)
    out = q_mdl.generate(**inputs, **T5_GEN_CONFIG)
    return q_tok.batch_decode(out, skip_special_tokens=True)

def correct_grammar(questions: List[str]) -> List[str]:
    inputs = ["gec: " + q for q in questions]
    enc = g_tok(inputs, return_tensors="pt", truncation=True, padding=True, max_length=128).to(q_dev)
    out = g_mdl.generate(**enc, num_beams=2, early_stopping=True, max_length=128)
    return g_tok.batch_decode(out, skip_special_tokens=True)

def extract_answers_with_qa(contexts: List[str], questions: List[str], originals: List[str]) -> List[str]:
    final = []
    for ctx, q, orig in zip(contexts, questions, originals):
        best, best_score = orig, 0.0
        for model in qa_models:
            try:
                output = model(question=q, context=ctx)
                if output["score"] > best_score:
                    best, best_score = output["answer"], output["score"]
            except Exception:
                continue
        final.append(best if best_score > 0.3 else orig)
    return final


def get_distractors(answers: List[str], pools: List[List[str]], top_k: int=3) -> List[List[str]]:
    # sbert = _load_sbert()
    ans_emb = sbert.encode(answers, convert_to_tensor=True)
    result = []
    for i,pool in enumerate(pools):
        if not pool:
            result.append([])
            continue
        d_emb = sbert.encode(pool, convert_to_tensor=True)
        sims = util.pytorch_cos_sim(ans_emb[i], d_emb).squeeze()
        top_idxs = sims.argsort(descending=True)[:top_k]
        result.append([pool[idx] for idx in top_idxs])
    return result


def run_model_quiz(goal: str, difficulty: str, num_q: int) -> Dict[str, Any]:
    if goal not in SUPPORTED_GOALS or difficulty not in SUPPORTED_DIFFICULTIES:
        raise ValueError(f"Invalid goal or difficulty: {goal}, {difficulty}")

    pool = filter_dataset(load_dataset(INPUT_PATH), goal, difficulty)
    if not pool:
        raise RuntimeError("No matching samples found")

    selected = random.sample(pool, min(num_q, len(pool)))
    contexts = [q["context"].strip() for q in selected]
    orig_ans = [q["correct_answer"].strip() for q in selected]
    distractor_pools = [q.get("distractors", []) for q in selected]

    mcq_count = max(1, int(num_q * 0.6))
    types = ["mcq"] * mcq_count + ["short_answer"] * (num_q - mcq_count)
    random.shuffle(types)

    questions = correct_grammar(generate_questions(contexts, orig_ans, goal, types))
    answers = extract_answers_with_qa(contexts, questions, orig_ans) if USE_QA else orig_ans
    dists = get_distractors(answers, distractor_pools)

    quiz = []
    for i, item in enumerate(selected):
        qtype = types[i]
        entry = {
            "type": qtype,
            "question": questions[i],
            "answer": answers[i] if qtype == "mcq" else contexts[i],
            "topic": item.get("topic", ""),
            "difficulty": item.get("difficulty", "")
        }
        if qtype == "mcq":
            opts = list(dict.fromkeys(dists[i] + [answers[i]]))
            random.shuffle(opts)
            entry["options"] = opts
        quiz.append(entry)

    return {"goal": goal, "difficulty": difficulty, "questions": quiz}
