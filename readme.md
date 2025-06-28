# Smart Quiz Generator 🔍📚

A production-ready, containerized microservice for generating intelligent MCQs and short-answer questions using local Transformer models (T5, SBERT), retrieval-based matching — designed for offline, goal-driven quiz generation.

---

## 📦 Project Structure

```
├── app/
│   ├── main.py                      # FastAPI app entry
│   ├── model_quiz/                  # Model-based quiz generator
│   ├── retrieval_quiz/              # Retrieval-based quiz generator
│   ├── models/                      # Local HuggingFace/Spacy models
│   ├── __pycache__/
│
├── data/                            # Domain-specific question banks
│   ├── Amazon SDE.json
│   ├── GATE ECE.json
│   └── Model.json
│
├── tests/                           # Pytest-based test suite
│   └── test_generate.py
│
├
│
├── Dockerfile                       # Docker config for containerization
├── config.json                      # Runtime config (goals, paths)
├── requirements.txt
├── .gitignore / .dockerignore
```

---

## ⚙️ Features

- ✅ Model-based question generation (T5-small)
- 🔁 Retrieval-based template question generation (TF-IDF + SBERT)
- 🧠 Sentence embedding via Sentence-Transformers
- 🧾 Grammar correction for question quality
- 📊 Named entity & POS-aware template rewriting
- 🧪 Test suite via `pytest`

---

## 🚀 Quickstart

### 1. Docker Build & Run

```bash
docker build -t smart-quiz-ai .
docker run -p 8000:8000 smart-quiz-ai
```

### 2. Local Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🧠 Core Modules

### 🔧 Entry Point

- `app/main.py` – FastAPI router loader

### 🤖 Model-based Generation

- `app/model_quiz/entrypoint.py` – Uses `t5-small` model
- `app/model_quiz/quiz_model.py` – Generates questions
- `app/models/t5-small/` – Local model dir

### 📄 Retrieval-based Generation

- `app/retrieval_quiz/entrypoint.py` – Semantic+TF-IDF quiz generator
- `app/retrieval_quiz/quiz_retrieval.py` – Template logic
- `app/retrieval_quiz/question_matcher.py` – Sentence matching
- `app/retrieval_quiz/topic_extractor.py` – Topic filter
- `app/models/sentence-transformer-model/` – Embedding model

### 🗃 Datasets

- `data/Model.json` – Central fine-tune dataset
- Domain sets: `data/Amazon SDE.json`, `data/GATE ECE.json`

---

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

