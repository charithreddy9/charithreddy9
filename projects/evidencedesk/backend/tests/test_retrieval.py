import numpy as np
import pytest
from backend.retrieval import EvidenceIndex, chunks, DEMO_DOCUMENTS

def test_chunking_no_empty_tail_and_overlap():
    assert chunks(" ".join(str(i) for i in range(10)),window=5,overlap=2) == [
        "0 1 2 3 4","3 4 5 6 7","6 7 8 9"
    ]

def test_invalid_chunk_configuration():
    with pytest.raises(ValueError):
        chunks("hello",window=2,overlap=2)

def test_lexical_ranking_and_exclusion():
    ix=EvidenceIndex()
    found=ix.search("What is the meal allowance?",top_k=2)
    assert found and found[0]["doc_id"]=="policy-travel"
    assert all(0 <= item["score"] <= 1 for item in found)

def test_embedded_synonym_retrieval_with_fake_vectors():
    class Encoder:
        def encode(self,texts):
            # Lightweight deterministic embeddings for unit testing semantic plumbing.
            def vector(t):
                txt=t.lower()
                return [1.,0.] if ("precipitation" in txt or "rain" in txt) else [0.,1.]
            return np.array([vector(text) for text in texts],dtype=np.float32)
    docs=[
        {"id":"a","title":"Weather","text":"Precipitation is expected this afternoon."},
        {"id":"b","title":"Cooking","text":"Onions should cook until soft."}
    ]
    ix=EvidenceIndex(docs,provider="sentence-transformers",encoder=Encoder())
    result=ix.search("Will it rain today?",top_k=1,minimum_score=.5)
    assert result[0]["doc_id"]=="a"
    assert result[0]["score"]==1.0

def test_page_metadata():
    ix=EvidenceIndex([{"id":"pdf","title":"Guide","text":"Section one Section two","pages":["First page content about travel policy.","Second page content about access controls."]}])
    assert ix.search("access controls",top_k=1)[0]["page"]==2
