"""Small transparent TF-IDF retriever with source-level provenance."""
from __future__ import annotations

import re
from uuid import uuid4
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEMO_DOCUMENTS = [
    {"id":"policy-travel","title":"Sample Travel & Expenses Policy","text":"Approved business travel expenses are reimbursable. Employees must submit an itemized receipt within 30 days of purchase. The meal allowance is $65 per day. Airfare costing more than $800 requires manager preapproval. All travel must be booked through the company travel portal. This is a fictional demonstration policy."},
    {"id":"policy-security","title":"Sample Security Handbook","text":"Production credentials must be stored in an approved secrets manager and must never be committed to source control. Multi-factor authentication is mandatory for company accounts. Report any suspected security incident to the security team within one hour. This is a fictional demonstration policy."},
    {"id":"policy-incident","title":"Sample Incident Response Playbook","text":"Priority-one incidents require on-call acknowledgment within ten minutes. A customer-impacting incident must have an assigned incident commander. After mitigation, the team publishes a post-incident report within five business days. This is a fictional demonstration policy."},
    {"id":"policy-data","title":"Sample Data Governance Guide","text":"Application diagnostic logs are retained for 90 days. Customer support exports must be encrypted and deleted after 14 days. Personal data access is limited by least-privilege permissions. Teams must not copy customer data into public AI tools. This is a fictional demonstration policy."},
]

def chunks(text: str, window: int = 90, overlap: int = 20) -> list[str]:
    words = re.findall(r"\S+", text)
    if not words:
        return []
    step = window - overlap
    return [" ".join(words[i:i + window]) for i in range(0, len(words), step) if words[i:i + window]]

class EvidenceIndex:
    def __init__(self, documents=None):
        self.documents = list(DEMO_DOCUMENTS if documents is None else documents)
        self._rebuild()

    def _rebuild(self):
        self.passages = [
            {"doc_id": doc["id"], "title": doc["title"], "chunk": j, "text": piece}
            for doc in self.documents for j, piece in enumerate(chunks(doc["text"]))
        ]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform([p["text"] for p in self.passages]) if self.passages else None

    def add_document(self, title: str, content: str):
        doc = {"id": str(uuid4()), "title": title.strip(), "text": content.strip()}
        self.documents.append(doc)
        self._rebuild()
        return {"id": doc["id"], "title": doc["title"], "chunks": len(chunks(doc["text"]))}

    def search(self, question: str, top_k: int = 3, minimum_score: float = 0.11):
        if self.matrix is None:
            return []
        query_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        order = sorted(range(len(scores)), key=lambda idx: (-float(scores[idx]), self.passages[idx]["doc_id"]))
        return [
            {**self.passages[i], "score": round(float(scores[i]), 4)}
            for i in order if scores[i] >= minimum_score
        ][:top_k]
