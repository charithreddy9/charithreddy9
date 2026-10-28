"""Single-instance document QA prototype with protected ingestion and citation checks."""
from __future__ import annotations

from contextlib import contextmanager
from io import BytesIO
import os
import secrets
import threading

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pypdf import PdfReader

from .llm import generate_grounded_answer
from .retrieval import DEMO_DOCUMENTS, EvidenceIndex, chunks
from .storage import DocumentStore

MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TEXT_CHARS = 50_000
MAX_PDF_PAGES = 60

class AskRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)
    top_k: int = Field(default=3, ge=1, le=5)
    generate: bool = False

class DocumentRequest(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    content: str = Field(min_length=80, max_length=MAX_TEXT_CHARS)

def extract_upload(filename: str, content: bytes) -> tuple[str, str, list[str] | None]:
    title = filename.replace("\\", "/").rsplit("/", 1)[-1].strip()[:120]
    if len(title) < 3 or len(content) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413 if len(content) > MAX_FILE_BYTES else 400, detail="File too large or invalid filename")
    extension = title.lower().rsplit(".", 1)[-1]
    if extension in {"txt", "md"}:
        try:
            extracted = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise HTTPException(400, "Please upload UTF-8 encoded text") from None
        pages = None
    elif extension == "pdf":
        try:
            pdf = PdfReader(BytesIO(content), strict=False)
            if len(pdf.pages) > MAX_PDF_PAGES:
                raise HTTPException(413, "PDF exceeds 60 pages")
            pages = [(page.extract_text() or "") for page in pdf.pages]
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "Invalid or unsupported PDF") from None
        extracted = "\n\n".join(pages)
    else:
        raise HTTPException(415, "Only .txt, .md and text-based .pdf are supported")
    extracted = extracted.replace("\x00", "").strip()
    if not 80 <= len(extracted) <= MAX_TEXT_CHARS:
        raise HTTPException(422, "Extractable text must contain 80–50,000 characters")
    if pages is not None and not any(page.strip() for page in pages):
        raise HTTPException(422, "Scanned PDFs require OCR, which is not supported")
    return title, extracted, pages

def create_app(documents=None, db_path=None, provider=None, encoder=None) -> FastAPI:
    selected = provider or os.getenv("RETRIEVAL_BACKEND", "tfidf")
    admin_token = os.getenv("ADMIN_TOKEN", "").strip()
    allow_public_upload = os.getenv("ALLOW_PUBLIC_UPLOAD", "").lower() == "true"
    allowed_origins = [u.strip() for u in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if u.strip()]

    app = FastAPI(title="EvidenceDesk API", version="0.2.0", docs_url="/docs" if os.getenv("ENABLE_API_DOCS", "true").lower() == "true" else None)
    app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_methods=["GET","POST","DELETE"], allow_headers=["Authorization","Content-Type"])
    store = DocumentStore(db_path or os.getenv("DATA_DB_PATH", "data/evidencedesk.sqlite3"), DEMO_DOCUMENTS if documents is None else documents)
    index = EvidenceIndex(store.list(), provider=selected, encoder=encoder)
    guard = threading.RLock()

    def require_read(authorization: str | None = Header(default=None)):
        if admin_token and not secrets.compare_digest(authorization or "", "Bearer " + admin_token):
            raise HTTPException(401, "Access token required")
        return True

    def require_write(authorization: str | None = Header(default=None)):
        require_read(authorization)
        if not admin_token and not allow_public_upload:
            raise HTTPException(403, "Document modification disabled. Set ADMIN_TOKEN before deployment.")
        return True

    @app.get("/api/health")
    def health():
        return {"status":"ok","retriever":selected,"documents":len(index.documents),"storage":"sqlite"}

    @app.get("/api/config")
    def config(_: bool = Depends(require_read)):
        return {"retriever":selected,"semantic_enabled":selected != "tfidf",
                "llm_available":bool(os.getenv("OPENAI_API_KEY")),
                "auth_required":bool(admin_token),"uploads_enabled":bool(admin_token or allow_public_upload),
                "file_types":[".txt",".md",".pdf"],"max_file_bytes":MAX_FILE_BYTES}

    @app.get("/api/documents")
    def list_documents(_: bool = Depends(require_read)):
        return [{"id":d["id"], "title":d["title"], "seeded":bool(d.get("seeded")),
                 "chunks":len([p for p in index.passages if p["doc_id"]==d["id"]])} for d in index.documents]

    def insert_document(title, content, pages=None):
        with guard:
            doc_id = store.insert(title.strip(), content.strip(), pages=pages)
            index.replace_documents(store.list())
            return {"id":doc_id,"title":title,"chunks":len([p for p in index.passages if p["doc_id"]==doc_id])}

    @app.post("/api/documents", status_code=201)
    def add_document(body: DocumentRequest, _: bool = Depends(require_write)):
        return insert_document(body.title, body.content)

    @app.post("/api/upload", status_code=201)
    async def upload_document(file: UploadFile = File(...), _: bool = Depends(require_write)):
        raw = await file.read(MAX_FILE_BYTES+1)
        title, text, pages = extract_upload(file.filename or "", raw)
        return insert_document(title, text, pages=pages)

    @app.delete("/api/documents/{document_id}")
    def delete_document(document_id: str, _: bool = Depends(require_write)):
        with guard:
            if not store.delete(document_id):
                raise HTTPException(404, "Document not found or protected demo document")
            index.replace_documents(store.list())
        return {"deleted":True,"id":document_id}

    @app.post("/api/ask")
    def ask(body: AskRequest, _: bool = Depends(require_read)):
        with guard:
            passages = index.search(body.question, body.top_k)
        if not passages:
            return {"answer":"I couldn't find enough supporting evidence in the indexed documents.",
                    "citations":[],"abstained":True,"mode":"abstained","retriever":selected}
        citations = [{"reference":f"[{i+1}]",**p} for i,p in enumerate(passages)]
        if body.generate:
            if not os.getenv("OPENAI_API_KEY"):
                raise HTTPException(503, "OPENAI_API_KEY is required for LLM synthesis; turn it off for extractive mode.")
            try:
                answer = generate_grounded_answer(body.question,citations)
            except Exception as exc:
                raise HTTPException(502, "LLM request failed; retry in extractive mode.") from exc
            if answer is None:
                return {"answer":"The available evidence was insufficient to generate a verifiably cited answer.",
                        "citations":citations,"abstained":True,"mode":"llm_abstained","retriever":selected}
            mode = "llm_grounded"
        else:
            p = citations[0]
            suffix = f", page {p['page']}" if p.get("page") else ""
            answer = f"Source excerpt from {p['title']}{suffix} {p['reference']}: {p['text']}"
            mode = "extractive"
        return {"answer":answer,"citations":citations,"abstained":False,"mode":mode,"retriever":selected}
    return app

app = create_app()
