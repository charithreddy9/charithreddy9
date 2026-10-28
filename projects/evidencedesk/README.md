# EvidenceDesk — Citation-Grounded AI Knowledge Workspace

**Stage:** runnable full-stack prototype. Not deployed; not production-ready.

A document-question-answering application using a **scikit-learn TF-IDF retriever**, **FastAPI**, and a responsive **React** interface. Supports text ingestion, source-grounded excerpts, abstention, and **optional LLM synthesis via the OpenAI API**.

## Architecture

```text
React/Vite UI ──► FastAPI ──► In-memory text ingestion + chunking
                              │
                         TF-IDF index
                              │
                      Cosine top-k retrieval
                              │
              ┌───────────────┴───────────────┐
          Extractive mode              Optional OpenAI mode
              └───────────────┬───────────────┘
                     Answer + source excerpts
```

### Why this project matters
It demonstrates end-to-end AI product engineering, retrieval evaluation, API design, grounded responses, validation, and front-end UX, rather than only a notebook. Four **fictional sample policies** are bundled for reproducible demos.

## Local setup

Requires Python 3.10+ and Node.js 20+.

```bash
# From this project directory
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r backend/requirements-dev.txt
uvicorn backend.app:app --reload --port 8000
```

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. API docs: http://localhost:8000/docs.

**Optional LLM mode:** set `OPENAI_API_KEY` in the backend environment, optionally `OPENAI_MODEL`. This invokes a paid external API. Without a key, extractive retrieval works fully offline. The app never exposes the key to the browser.

## APIs

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/api/health` | API/index health |
| GET | `/api/documents` | List indexed document titles |
| POST | `/api/documents` | Ingest an 80–12,000-character text document |
| POST | `/api/ask` | Retrieve sources and return answer; `generate: true` enables LLM |

## Evaluation and tests

```bash
python -m pytest backend/tests -q
python -m backend.evaluate
```

The evaluation performs **hit@3 checks against five hand-written questions** with known source IDs. This toy set is only a development regression check—not a validated production retrieval benchmark. A missing match leads to explicit abstention; overlapping keywords can still cause false positives.

## Tradeoffs and next milestones

- In-memory, unauthenticated text ingestion is **local demo only**; every restart removes user uploads. Do not upload private or sensitive documents.
- TF-IDF is lexical, not semantic embedding-based retrieval; synonym and multi-hop questions can fail.
- LLM citations are prompt-guided, **not independently verified**; downstream citation validation is future work.
- Next: persisted document storage, PDF parsing, embeddings + reranking, a labeled retrieval benchmark, per-user authorization, rate limits, prompt-injection tests, containerization, and deployment.
