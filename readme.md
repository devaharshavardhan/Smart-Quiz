# Smart Quiz Generator 🔍📚

A production-ready, containerized microservice for generating intelligent MCQs and short-answer questions using local Transformer models (T5, SBERT), and retrieval-based matching — designed for offline, goal-driven quiz generation.

---

## 📁 Project Structure

```bash
Smart-Quiz/
├── app/
│   ├── main.py                      # FastAPI app entrypoint
│   ├── model_quiz/                  # Model-based generation logic
│   │   ├── config_model.py
│   │   ├── data_model.py
│   │   ├── entrypoint.py
│   │   ├── loaders_model.py
│   │   ├── quiz_model.py
│   │   └── utils_model.py
│   ├── retrieval_quiz/              # Retrieval-based generation logic
│   │   ├── entrypoint.py
│   │   ├── question_matcher.py
│   │   ├── quiz_retrieval.py
│   │   ├── retrieval_config.py
│   │   └── topic_extractor.py
│   └── models/                      # ⚠️ Large models not included in Git
│       └── readme.md                # Google Drive download link & structure
├── data/                            # Question datasets
│   ├── Amazon SDE.json
│   ├── AWS(R).json
│   ├── CS(R).json
│   ├── GATE CSE.json
│   ├── GATE ECE.json
│   ├── ML(R).json
│   └── Model.json                   # Central dataset for fine-tuning/testing
├── tests/
│   └── test_generate.py             # Unit test for generation pipeline
├── config.json                      # Config: goals, difficulty, mode
├── schema.json                      # API input/output schemas
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container configuration
├── .gitignore
├── .dockerignore
└── README.md                        # You're here 🚀
```

---

## ⚙️ Features

- ✅ **Model-based generation** using T5-small (offline)
- 🔁 **Retrieval-based WH-template generation** (TF-IDF + SBERT + NER)
- 🧠 **Semantic distractor generation** using Sentence-BERT
- 🧾 **Grammar correction** for refined questions
- 🔀 **Dynamic mode switching** via `config.json`
- 🧪 **Testable** via `pytest`
- 📦 **Fully Dockerized** & offline-ready

---

## 🚀 Quickstart

### 1️⃣ Docker Build & Run

```bash
docker build -t smart-quiz-ai .
docker run -p 8000:8000 smart-quiz-ai
```

### 2️⃣ Local Development

### 🖥️ Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/devaharshavardhan/Smart-Quiz.git
cd Smart-Quiz

# 2. Download large model files (⚠️ NOT included in the repo)
#    📄 Follow the instructions in: app/models/readme.md

# ✅ Example: Final folder structure after extracting downloaded models
# app/models/
# ├── t5-small/
# ├── all-MiniLM-L6-v2/
# ├── grammar-corrector/
# ├── qa-distil/
# ├── qa-roberta-squad2/
# ├── spacy/
# └── sentence-transformer-model/

# 3. (Optional) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate         # On Windows: .venv\Scripts\activate

# 4. Install all dependencies
pip install -r requirements.txt

# 5. Start the FastAPI development server
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 Core Modules

### 🔧 Entry Point

- `app/main.py` — FastAPI app entry and router logic.

---

### 🤖 Model-Based Generation (`app/model_quiz/`)

| Module              | Purpose                                               |
|---------------------|--------------------------------------------------------|
| `entrypoint.py`     | API entry for model-based generation                  |
| `quiz_model.py`     | T5-based question generator (MCQ & short-answer)      |
| `data_model.py`     | Filters dataset by goal/difficulty                    |
| `loaders_model.py`  | Loads T5, SBERT, grammar correction models            |
| `config_model.py`   | Reads config for generation mode                      |
| `utils_model.py`    | Grammar correction + semantic distractor utils        |

📦 Models Used:

- `t5-small/` – Text-to-text model for question generation  
- `all-MiniLM-L6-v2/` – SBERT model for semantic distractors  
- `grammar-corrector/` – Model to refine question grammar  
- `qa-distil/` – DistilBERT-based QA model  
- `qa-roberta-squad2/` – Roberta QA model for longer answers  

---

### 📄 Retrieval-Based Generation (`app/retrieval_quiz/`)

| Module                  | Purpose                                           |
|--------------------------|---------------------------------------------------|
| `entrypoint.py`         | API handler for retrieval mode                    |
| `quiz_retrieval.py`     | WH-template generator using selected sentences    |
| `question_matcher.py`   | TF-IDF + SBERT matcher                            |
| `topic_extractor.py`    | Named Entity Recognition via spaCy               |
| `retrieval_config.py`   | Configuration loader for retrieval mode          |

📦 Models Used:

- `sentence-transformer-model/` — SBERT-based similarity
- `spacy/` — spaCy NER model for topic extraction

---

### 🗃 Datasets (`data/`)

| File                 | Description                            |
|----------------------|----------------------------------------|
| `Model.json`         | Master training/evaluation dataset     |
| `Amazon SDE.json`    | Domain-specific questions (SDE)        |
| `AWS(R).json`        | AWS-related question bank              |
| `GATE CSE.json`      | GATE CSE questions                     |
| `GATE ECE.json`      | GATE ECE questions                     |
| `CS(R).json`         | General computer science set           |
| `ML(R).json`         | Machine learning question set          |

---

## 🧪 Testing

Run all unit tests using:

```bash
pytest tests/test_generate.py
```

---

## 📚 References

### 🔧 Libraries

- **FastAPI** – [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)  
- **Uvicorn** – [https://www.uvicorn.org](https://www.uvicorn.org)  
- **Transformers (HuggingFace)** – [https://huggingface.co/transformers](https://huggingface.co/transformers)  
- **Sentence-Transformers** – [https://www.sbert.net](https://www.sbert.net)  
- **PyTorch** – [https://pytorch.org](https://pytorch.org)  
- **scikit-learn** – [https://scikit-learn.org](https://scikit-learn.org)  
- **spaCy** – [https://spacy.io](https://spacy.io)  

### 🧠 Core Models

- **T5** – Raffel et al., JMLR 2020  
- **SBERT** – Reimers & Gurevych, EMNLP 2019  
- **TF-IDF + Cosine Similarity** – Salton & Buckley, 1988  

---

## 🧾 License

**Internal License** — For institutional/internal use only.  
You may use, modify, and distribute this project *within* your organization with credit.  
**External distribution or commercial use requires prior written permission.**

---

## 🙏 Acknowledgements

Built with:

- ❤️ HuggingFace Transformers  
- ⚙️ FastAPI & Uvicorn  
- 🧪 PyTorch & Sentence Transformers  
- 📚 spaCy NLP pipeline  
