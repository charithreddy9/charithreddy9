"""SQLite document persistence. Suitable for a single-instance personal demo."""
from __future__ import annotations
import json
import sqlite3
import threading
from pathlib import Path
from uuid import uuid4

class DocumentStore:
    def __init__(self, path: str, seed_documents: list[dict]):
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.RLock()
        with self.lock:
            self.conn.execute("""CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL,
                pages_json TEXT, seeded INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")
            for doc in seed_documents:
                self.conn.execute(
                    "INSERT OR IGNORE INTO documents(id,title,content,pages_json,seeded) VALUES(?,?,?,?,1)",
                    (doc["id"], doc["title"], doc["text"], json.dumps(doc.get("pages")))
                )
            self.conn.commit()

    def list(self):
        with self.lock:
            rows = self.conn.execute("SELECT id,title,content,pages_json,seeded FROM documents ORDER BY seeded DESC, created_at, id").fetchall()
        return [
            {"id": row[0], "title": row[1], "text": row[2], **({"pages": json.loads(row[3])} if row[3] and json.loads(row[3]) else {}), "seeded": bool(row[4])}
            for row in rows
        ]

    def insert(self, title: str, content: str, pages=None):
        doc_id = str(uuid4())
        with self.lock:
            self.conn.execute("INSERT INTO documents(id,title,content,pages_json) VALUES (?,?,?,?)",
                              (doc_id,title,content,json.dumps(pages) if pages else None))
            self.conn.commit()
        return doc_id

    def delete(self, doc_id: str) -> bool:
        with self.lock:
            cursor = self.conn.execute("DELETE FROM documents WHERE id=? AND seeded=0", (doc_id,))
            self.conn.commit()
        return cursor.rowcount > 0
