import time
import random
import torch
from functools import lru_cache
from transformers import T5ForConditionalGeneration, T5TokenizerFast, AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sentence_transformers import SentenceTransformer
from app.model_quiz.config_model import T5_MODEL_PATH, GRAMMAR_MODEL_PATH, QA_MODEL_PATHS, SBERT_PATH

@lru_cache()
def load_t5():
    tok = T5TokenizerFast.from_pretrained(T5_MODEL_PATH, local_files_only=True)
    mdl = T5ForConditionalGeneration.from_pretrained(T5_MODEL_PATH, local_files_only=True)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    mdl.to(dev)
    return tok, mdl, dev

@lru_cache()
def load_grammar():
    tok = AutoTokenizer.from_pretrained(GRAMMAR_MODEL_PATH, local_files_only=True)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(GRAMMAR_MODEL_PATH, local_files_only=True)
    _, _, dev = load_t5()
    mdl.to(dev)
    return tok, mdl

@lru_cache()
def load_qa():
    return [pipeline("question-answering", model=path, tokenizer=path, local_files_only=True) for path in QA_MODEL_PATHS.values()]

@lru_cache()
def load_sbert():
    return SentenceTransformer(SBERT_PATH)
