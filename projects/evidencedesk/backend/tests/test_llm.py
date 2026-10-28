from types import SimpleNamespace
from backend.llm import generate_grounded_answer

CITES=[{"reference":"[1]","title":"Demo Travel Policy","text":"Receipts are due within 30 days.","page":2}]

class FakeClient:
    def __init__(self,answer):
        self.answer=answer
        self.request=None
        self.responses=self
    def create(self,**kwargs):
        self.request=kwargs
        return SimpleNamespace(output_text=self.answer)

def test_cited_answer():
    client=FakeClient("Submit receipts within 30 days [1].")
    output=generate_grounded_answer("When?",CITES,client=client)
    assert output.endswith("[1].")
    assert "untrusted" in client.request["instructions"].lower()
    assert 'Demo Travel Policy' in client.request["input"]

def test_rejects_unknown_reference():
    assert generate_grounded_answer("When?",CITES,client=FakeClient("As written [9].")) is None

def test_rejects_uncited():
    assert generate_grounded_answer("When?",CITES,client=FakeClient("In 30 days.")) is None

def test_declines_insufficient_evidence():
    assert generate_grounded_answer("When?",CITES,client=FakeClient("INSUFFICIENT_EVIDENCE")) is None

def test_empty_citations_make_no_llm_call():
    assert generate_grounded_answer("When?",[],client=FakeClient("Something [1].")) is None
