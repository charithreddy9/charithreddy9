# EvidenceDesk — Full-Stack AI Document Intelligence

**Status: developing portfolio prototype · NOT yet publicly deployed · NOT production-secure**

Document-question answering with **FastAPI + React**, SQLite-backed source records, PDF/TXT/Markdown ingestion, and transparent retrieval. Three *explicitly configured* retrieval backends:

- `tfidf`: fully offline lexical retrieval; default, works without embedding model or API keys.
- `sentence-transformers`: **real local semantic embeddings** (default all-MiniLM-L6-v2). Requires `backend/requirements-semantic.txt` and downloading model weights during initial setup.
- `openai`: **real hosted semantic embeddings** via `text-embedding-3-small`; requires paid `OPENAI_API_KEY`.

Optional **OpenAI LLM** synthesis is prompted to cite retrieved passages. Citation numbers are validated; factual entailment is **not** independently verified. Uncited answers and unknown citation markers cause abstention.

## Architecture

```text
Browser / React ─► Nginx (proxy /api) ─► FastAPI ─► SQLite documents
                                              │
                                   Page-aware text chunking
                                              │
                                   Explicitly selected retriever
                        ┌─────────────────────┼──────────────────────┐
                    TF-IDF                Local embeddings       OpenAI embeddings
                        └─────────────────────┼──────────────────────┘
                                     Ranked source passages
                                              │
                              Extractive answer OR optional LLM
                                              │
                                Validated reference markers [1]
```

Sources are stored persistently. The in-process vector index is rebuilt on startup and after uploads or deletion; **embeddings are not yet persisted**. This is a single-instance demo, not a scalable vector database system.

## Quick start: Docker (recommended)

From `projects/evidencedesk`:

```bash
cp .env.example .env
# Edit .env and replace ADMIN_TOKEN with a long random secret
docker compose up --build
```

Browse **http://localhost:8080**. Compose intentionally binds to loopback only; use a TLS-terminating reverse proxy and additional hardening for any public deployment. Paste the same `ADMIN_TOKEN` into the app's token field to access protected endpoints and upload documents. The token stays in React state (not local storage). Do **not** embed the token in the frontend bundle.

For local embeddings, change `RETRIEVAL_BACKEND=sentence-transformers` and `INSTALL_SEMANTIC=true` in `.env`, then rebuild. First model download requires internet and increases image size/startup latency.

For OpenAI embeddings, use `RETRIEVAL_BACKEND=openai` and set `OPENAI_API_KEY`. LLM synthesis uses the same server-side key and can incur charges.

## Local development without Docker

Requires Python 3.11+ and Node.js 22+.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r backend/requirements-dev.txt
# For local semantic inference, also install: pip install -r backend/requirements-semantic.txt
# Optional: set ADMIN_TOKEN in your environment before launching
uvicorn backend.app:app --reload --port 8000
```

In a second terminal:

```bash
cd frontend
npm install
# Direct local backend from Vite: create frontend/.env.local containing:
# VITE_API_BASE_URL=http://localhost:8000
npm run dev
```

API reference in development: **http://localhost:8000/docs**.

## API

| Endpoint | Notes |
| --- | --- |
| `GET /api/health` | Unauthenticated health |
| `GET /api/config` | Retriever and feature capability flags |
| `GET /api/documents` | Document list; titles/IDs and chunk counts |
| `POST /api/upload` | Ingest PDF, TXT, or MD, max 2 MiB; write protection applies |
| `POST /api/documents` | JSON text ingestion |
| `DELETE /api/documents/{id}` | Delete user-imported docs (seed documents protected) |
| `POST /api/ask` | Top-k retrieval; optional `generate: true` LLM synthesis |

`ADMIN_TOKEN` protects read/write endpoints via `Authorization: Bearer …`; **without a token, read-only sample mode is enabled by default**. In a public deployment, always set a strong token. This is basic single-tenant protection, not production identity or RBAC.

## Quality checks

```bash
python -m pytest backend/tests -q
python -m backend.evaluate
cd frontend && npm run build
```

CI runs offline TF-IDF tests, including a deterministic fake encoder test for the semantic retrieval integration. Real external embedding model loading and hosted API calls are **not covered in CI** and must be evaluated separately.

## Limitations and roadmap

- Four **fictional sample policies** and a five-question toy retrieval evaluation. No claims of real-world benchmark accuracy.
- PDF extraction only handles text-based PDFs, not scanned documents/OCR.
- TF-IDF or embedding cosine score is **not a calibrated confidence score**. Retrieval thresholds are development heuristics, and semantic search can return semantically related but irrelevant chunks.
- LLM citation marker validation does not guarantee factual accuracy; rigorous faithfulness evaluation and adversarial prompt-injection tests remain to be done.
- SQLite and in-process vector index are single-instance; process restarts rebuild the model index.
- Shared admin token, no per-user authorization, rate limits, virus scanning, document redaction, audit logs, or distributed storage. **Do not ingest sensitive or regulated documents in an untrusted deployment.**
- Planned next: persistent vector store (pgvector), reranking, evaluated semantic retrieval on benchmark data, OAuth/OIDC login, durable ingest jobs, audit trails, and public deployment with hardened ingress.

**This repository lives under `charithreddy9/charithreddy9/projects/evidencedesk` until a dedicated `EvidenceDesk-AI` repository is created.**
