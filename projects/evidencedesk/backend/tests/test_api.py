from fastapi.testclient import TestClient
from backend.app import create_app

def test_health():
    assert TestClient(create_app()).get("/api/health").json()["documents"] == 4

def test_source_grounded_retrieval():
    res = TestClient(create_app()).post("/api/ask", json={"question":"What is the receipt reimbursement deadline?"})
    assert res.status_code == 200
    body = res.json()
    assert body["abstained"] is False
    assert body["citations"][0]["doc_id"] == "policy-travel"
    assert body["mode"] == "extractive"

def test_abstains_when_no_evidence():
    body = TestClient(create_app()).post("/api/ask", json={"question":"What is the quantum banana temperature?"}).json()
    assert body["abstained"] is True
    assert body["citations"] == []

def test_ingestion_then_retrieval():
    client = TestClient(create_app())
    content = "The lunar observatory is open to employees on Tuesdays between 8 and 11 in the morning. " * 3
    assert client.post("/api/documents", json={"title":"Observatory schedule","content":content}).status_code == 201
    result = client.post("/api/ask", json={"question":"When is the lunar observatory open?"}).json()
    assert result["citations"][0]["title"] == "Observatory schedule"

def test_input_validation():
    assert TestClient(create_app()).post("/api/ask", json={"question":"hi"}).status_code == 422

def test_llm_requires_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    res = TestClient(create_app()).post("/api/ask", json={"question":"What is the meal allowance?", "generate":True})
    assert res.status_code == 503
