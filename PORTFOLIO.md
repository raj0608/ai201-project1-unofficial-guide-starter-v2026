# 📘 Project 1 — Unofficial Guide RAG System: Skills & Technologies

> **Note:** This is a personal portfolio reflection. The graded submission is `README.md`.

---

## 🔍 What I Built

A **Retrieval-Augmented Generation (RAG)** pipeline that answers natural-language questions against a private corpus of documents. A user asks anything about the ingested material and gets a grounded, cited answer — or a clean refusal if the corpus doesn't cover the topic.

---

## 🛠️ Tools & Technologies

| Category | Tool / Library | Purpose |
|---|---|---|
| **LLM API** | Google Gemini (`google-genai` ≥1.0) | Answer generation from retrieved context |
| **Vector Store** | ChromaDB (`chromadb` ≥0.6) | Local embedding storage and cosine-similarity search |
| **Embeddings** | `all-MiniLM-L6-v2` (ONNX via ChromaDB) | Converts text chunks into 384-dimensional vectors |
| **Web Server** | Flask + Gunicorn | Exposes the pipeline as an HTTP API via `serve.py` |
| **Env Management** | python-dotenv | Loads API keys from `.env` without hardcoding secrets |
| **Keyword Search** | rank-bm25 | Optional BM25 hybrid search layer for improved recall |
| **Language** | Python 3.11–3.13 | Core implementation language |

---

## ⚙️ Architecture & Key Design Decisions

- **Chunking** — Documents are split into overlapping character windows (`CHUNK_SIZE=800`, `CHUNK_OVERLAP=120`) so context is never cut at an awkward sentence boundary.
- **Relevance Gate** — A cosine distance threshold (`THRESHOLD=0.33`) hard-stops the pipeline before generation if no retrieved chunk is a close enough match. This prevents hallucinated answers on out-of-scope questions.
- **Rate Limiting** — A built-in request budget (`SESSION_REQUEST_BUDGET=300`, `REQUESTS_PER_MINUTE=30`) with exponential backoff on 429s guards against quota exhaustion.
- **Response Caching** — Disk-based cache (`CACHE_ENABLED`) avoids redundant API calls during development and evals.
- **Automated Evaluation** — `run_eval.py` + `scorer.py` automate quality scoring over a question set so threshold and chunking decisions are data-driven rather than guesswork.

---

## 🧠 Skills Learned

### AI / ML Concepts
- How RAG works end-to-end: ingest → chunk → embed → store → retrieve → generate
- The role of cosine distance in semantic search and how to tune a relevance threshold empirically
- Trade-offs between chunk size, overlap, and retrieval quality
- Why and when to gate generation (refusing gracefully vs. hallucinating)
- BM25 keyword search as a complement to dense vector retrieval (hybrid RAG)
- Evaluating generation quality programmatically with a scorer

### Software Engineering
- Building a modular Python pipeline where each stage (`ingest`, `store`, `retrieve`, `generate`) is independently testable and replaceable
- Designing a dual interface: CLI tool (`app.py`) and HTTP API (`serve.py`) backed by the same logic
- Writing an automated eval harness and using its output to drive tuning decisions
- Dependency pinning strategy — why upper-bound pins prevent mid-term breakage in shared environments

### Tools & Workflow
- ChromaDB local vector database: collection setup, upserting, querying
- Google Gemini API integration via `google-genai` SDK
- Flask application structure and production serving with Gunicorn
- Environment variable management with `.env` and `python-dotenv`
- Threshold-based quality gates in AI pipelines

---

## 📂 Key Files

| File | Role |
|---|---|
| `ingest.py` | Reads raw corpus documents from disk |
| `chunker.py` | Splits documents into overlapping character-level chunks |
| `store.py` | Embeds chunks and upserts them into ChromaDB |
| `gate.py` | Relevance threshold check — blocks generation if nothing is close |
| `generate.py` | Calls Gemini to produce the final grounded answer |
| `run_eval.py` | Runs the automated evaluation harness |
| `scorer.py` | Scores generated answers against expected outputs |
| `serve.py` | Flask HTTP server wrapping the full pipeline |
| `config.py` | All tunable constants (chunk size, threshold, model, rate limits) |
