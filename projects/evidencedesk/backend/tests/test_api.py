import pytest
from fastapi.testclient import TestClient
from backend.app import create_app
from backend.retrieval import DEMO_DOCUMENTS

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.delenv("ADMIN_TOKEN", raising=False)
    monkeypatch.delenv("ALLOW_PUBLIC_UPLOAD", raising=False)
    return TestClient(create_app(db_path=str(tmp_path / "demo.sqlite3"), provider="tfidf"))

def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["documents"] == 4
    assert r.json()["retriever"] == "tfidf"

def test_grounded_lexical_retrieval(client):
    body = client.post("/api/ask", json={"question":"What is the meal allowance?"}).json()
    assert body["mode"] == "extractive"
    assert body["citations"][0]["doc_id"] == "policy-travel"
    assert "[1]" in body["answer"] and "$65" in body["answer"]

def test_abstention(client):
    body = client.post("/api/ask", json={"question":"What is the quantum banana temperature?"}).json()
    assert body["abstained"] is True
    assert body["citations"] == []

def test_input_validation(client):
    assert client.post("/api/ask", json={"question":"hi"}).status_code == 422
    assert client.post("/api/ask", json={"question":"What are travel rules?","top_k":9}).status_code == 422

def test_writes_disabled_without_admin_token(client):
    body={"title":"Observatory schedule","content":"The observatory is open on Tuesdays. "*5}
    assert client.post("/api/documents",json=body).status_code == 403

def test_requires_llm_key(client, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY",raising=False)
    r=client.post("/api/ask",json={"question":"What is the meal allowance?","generate":True})
    assert r.status_code == 503

def test_auth_upload_delete_persistence(tmp_path, monkeypatch):
    monkeypatch.setenv("ADMIN_TOKEN","testing-secret")
    monkeypatch.delenv("ALLOW_PUBLIC_UPLOAD",raising=False)
    db=str(tmp_path / "saved.sqlite3")
    client=TestClient(create_app(db_path=db,provider="tfidf"))
    headers={"Authorization":"Bearer testing-secret"}
    assert client.get("/api/documents").status_code == 401
    assert client.post("/api/ask",json={"question":"What is the meal allowance?"}).status_code == 401
    assert client.post("/api/upload",files={"file":("notes.txt",b"hello world"*20,"text/plain")}).status_code == 401
    content=("The observatory opens every Tuesday from nine to noon. " * 6).encode()
    r=client.post("/api/upload",headers=headers,files={"file":("observatory.txt",content,"text/plain")})
    assert r.status_code == 201, r.text
    doc_id=r.json()["id"]
    qa=client.post("/api/ask",headers=headers,json={"question":"When does the observatory open?"})
    assert qa.status_code == 200 and qa.json()["citations"][0]["doc_id"] == doc_id
    restarted=TestClient(create_app(db_path=db,provider="tfidf"))
    assert doc_id in [d["id"] for d in restarted.get("/api/documents",headers=headers).json()]
    assert restarted.delete(f"/api/documents/{doc_id}",headers=headers).status_code == 200
    assert restarted.delete("/api/documents/policy-travel",headers=headers).status_code == 404

def test_rejects_bad_upload(tmp_path, monkeypatch):
    monkeypatch.setenv("ADMIN_TOKEN","secret")
    client=TestClient(create_app(db_path=str(tmp_path/"db.sqlite3")))
    headers={"Authorization":"Bearer secret"}
    assert client.post("/api/upload",headers=headers,files={"file":("malware.exe",b"A"*100,"application/octet-stream")}).status_code==415
    assert client.post("/api/upload",headers=headers,files={"file":("broken.pdf",b"not a PDF","application/pdf")}).status_code==400
    assert client.post("/api/upload",headers=headers,files={"file":("huge.txt",b"x"*(2*1024*1024+1),"text/plain")}).status_code==413
    assert client.post("/api/upload",headers=headers,files={"file":("short.txt",b"tiny","text/plain")}).status_code==422

def test_config_describes_semantic_mode(tmp_path,monkeypatch):
    import numpy as np
    class FakeEncoder:
        def encode(self,texts):
            return np.asarray([[1.,0.] if "security" in t.lower() else [0.,1.] for t in texts])
    app=create_app(db_path=str(tmp_path/"sem.sqlite"),provider="sentence-transformers",encoder=FakeEncoder())
    result=TestClient(app).get("/api/config")
    assert result.status_code==200 and result.json()["semantic_enabled"] is True
