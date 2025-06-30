# Smart Quiz Generator 🔍📚

A production-ready, containerized microservice for generating intelligent MCQs and short-answer questions using local Transformer models (T5, SBERT), retrieval-based matching — designed for offline, goal-driven quiz generation.

---

## 📦 Project Structure

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
│   │
│   ├── retrieval_quiz/              # Retrieval-based generation logic
│   │   ├── entrypoint.py
│   │   ├── question_matcher.py
│   │   ├── quiz_retrieval.py
│   │   ├── retrieval_config.py
│   │   └── topic_extractor.py
│   │
│   └── models/                      # ⚠️ Large models not included in Git
│       └── readme.md                # Contains Google Drive download link & structure
│
├── data/                            # Question datasets
│   ├── Amazon SDE.json
│   ├── AWS(R).json
│   ├── CS(R).json
│   ├── GATE CSE.json
│   ├── GATE ECE.json
│   ├── ML(R).json
│   └── Model.json                   # Central dataset for fine-tuning/testing
│
├── tests/
│   └── test_generate.py             # Unit test for generation pipeline
│
├── config.json                      # Config: goals, difficulty, mode
├── schema.json                      # API input/output schemas
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container configuration
├── .gitignore / .dockerignore
└── README.md                        # You're here 🚀


## ⚙️ Features

- ✅ **Model-based question generation** using T5-small (offline)
- 🔁 **Retrieval-based WH-template generation** (TF-IDF + SBERT + NER)
- 🧠 **Semantic distractor generation** using Sentence-BERT
- 🧾 **Grammar correction** for refined questions
- 🔀 Mode switching via `config.json`
- 🧪 Testable via `pytest`
- 📦 Docker-ready & fully offline

## 🚀 Quickstart

### 1. Docker Build & Run

```bash
docker build -t smart-quiz-ai .
docker run -p 8000:8000 smart-quiz-ai
```

### 2. Local Run

# 1. Clone the repository
git clone https://github.com/devaharshavardhan/Smart-Quiz.git
cd Smart-Quiz

# 2. Download large models manually
#    ⚠️ Models are NOT committed due to size limits.
#    📄 Follow the download link and structure described in:
#    > app/models/readme.md

# Example (manual step):
# - Download the ZIP from the Google Drive link in readme.md
# - Extract all model folders into: app/models/
# - Final structure should look like:
#   app/models/
#   ├── t5-small/
#   ├── all-MiniLM-L6-v2/
#   ├── grammar-corrector/
#   └── ...

# 3. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate

# 4. Install all required dependencies
pip install -r requirements.txt

# 5. Run the FastAPI development server
uvicorn app.main:app --reload


---
## 🧠 Core Modules

### 🔧 Entry Point

- `app/main.py` – FastAPI app entry point and router configuration

---

### 🤖 Model-based Generation (`app/model_quiz/`)

- `entrypoint.py` – Handles API requests for model-based question generation
- `quiz_model.py` – Generates MCQs and short-answer questions using T5
- `data_model.py` – Filters the dataset by `goal` and `difficulty`
- `loaders_model.py` – Loads local T5, SBERT, and grammar correction models
- `config_model.py` – Parses configuration for model generation
- `utils_model.py` – Utilities: grammar correction, semantic distractor filtering

📦 Models Used:
- `t5-small/` – T5 model for question generation
- `all-MiniLM-L6-v2/` – SBERT model for distractor generation
- `grammar-corrector/` – Grammar correction model
- `qa-distil/` – Lightweight QA model (DistilBERT)
- `qa-roberta-squad2/` – Roberta-based QA model

---

### 📄 Retrieval-based Generation (`app/retrieval_quiz/`)

- `entrypoint.py` – Controls the retrieval-based generation flow
- `quiz_retrieval.py` – WH-question generator using template logic
- `question_matcher.py` – TF-IDF + SBERT based context matcher
- `topic_extractor.py` – Extracts topics/entities using spaCy NER
- `retrieval_config.py` – Reads and applies config settings for retrieval mode

📦 Models Used:
- `sentence-transformer-model/` – Used for semantic similarity scoring
- `spacy/` – spaCy model for entity recognition (NER)

---

### 🗃 Datasets (`data/`)

- `Model.json` – Master dataset used for training/fine-tuning/testing
- Domain-specific question sets:
  - `Amazon SDE.json`
  - `AWS(R).json`
  - `CS(R).json`
  - `GATE CSE.json`
  - `GATE ECE.json`
  - `ML(R).json`

## 🧪 Testing

```bash
pytest tests/test_generate.py
```

---

## 📚 References

### Core Libraries & Frameworks

**Python 3.10+** Python Software Foundation. *Python Language Reference, version 3.10*.

**FastAPI** Ramírez, S. *FastAPI: high performance, easy to learn, fast to code, ready for production.* (2021). [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

**Uvicorn** Tom Christie et al. *Uvicorn: Lightning-fast ASGI server.* (2021). [https://www.uvicorn.org](https://www.uvicorn.org)

**PyTorch** Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., ... & Chintala, S. (2019). *PyTorch: An Imperative Style, High-Performance Deep Learning Library*. *Advances in Neural Information Processing Systems*, 32.

**Transformers (Hugging Face)** Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., ... & Rush, A. M. (2020). *Transformers: State-of-the-art Natural Language Processing*. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations*, 38–45.

**Sentence-Transformers** Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing*, 3982–3992.

**scikit-learn** Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011). *Scikit-learn: Machine Learning in Python*. *Journal of Machine Learning Research*, 12, 2825–2830.

**spaCy** Explosion AI. (2020). *spaCy: Industrial-strength Natural Language Processing*. Retrieved from [https://spacy.io](https://spacy.io)

### Key Models & Techniques

**T5 (Text-to-Text Transfer Transformer)** Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., ... & Liu, P. J. (2020). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. *Journal of Machine Learning Research*, 21(140), 1–67.

**TF-IDF & Cosine Similarity** Salton, G., & Buckley, C. (1988). *Term-weighting approaches in automatic text retrieval*. *Information Processing & Management*, 24(5), 513–523.

### Data & Datasets

**Domain Question Banks** Organization-curated JSON files (e.g., `Amazon SDE.json`, `GATE ECE.json`), containing 300+ question samples per domain.

**Model Fine-tuning Dataset** Dataset: `data/Model.json`, containing context–question pairs used to fine-tune the T5 model.

**config.json** Configuration file defining runtime parameters, supported goals, difficulties, model paths, and dataset mappings.

### Configuration & Utilities

**LRU Cache** Python `functools.lru_cache` for efficient model loading and caching.

**Random Seeding** Python’s `random.seed()` and `torch.manual_seed()` for reproducibility.

### Deployment & Packaging

**Docker** Docker, Inc. *Docker: Empowering apps, environments, and containers.* (2020). Retrieved from [https://www.docker.com](https://www.docker.com)

### Citation Format Examples (BibTeX)

```bibtex
@article{raffel2020t5,
  title   = {Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer},
  author  = {Raffel, Colin and Shazeer, Noam and Roberts, Adam and Lee, Katherine and Narang, Sharan and Matena, Michael and Zhou, Yanqi and Li, Wei and Liu, Peter J.},
  journal = {Journal of Machine Learning Research},
  volume  = {21},
  number  = {140},
  pages   = {1--67},
  year    = {2020}
}

@inproceedings{reimers2019sentence,
  title     = {Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks},
  author    = {Reimers, Nils and Gurevych, Iryna},
  booktitle = {Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing},
  pages     = {3982--3992},
  year      = {2019}
}

@article{pedregosa2011scikit,
  title   = {Scikit-learn: Machine Learning in Python},
  author  = {Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V. and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P. and Weiss, R. and Dubourg, V. and Passos, A. and Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, É.},
  journal = {Journal of Machine Learning Research},
  volume  = {12},
  pages   = {2825--2830},
  year    = {2011}
}

@misc{explosion_spacy,
  title  = {{spaCy}: Industrial-strength Natural Language Processing},
  author = {Explosion AI},
  year   = {2020},
  url    = {https://spacy.io}
}
```

---

## 📄 License

Internal License – For institutional or internal use only.You may use, modify, and distribute this project within your organization or institution with credit to the original author. External distribution or commercial use requires prior written permission.

---

## 🙏 Acknowledgements

Built with:

- ❤️ HuggingFace Transformers
- ⚙️ FastAPI & Uvicorn
- 🧪 PyTorch & Sentence Transformers
- 📚 spaCy NLP pipeline

