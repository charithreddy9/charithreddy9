"""Toy retrieval hit@k smoke benchmark; not a production quality assessment."""
import os
from .retrieval import EvidenceIndex

CASES = [
    ("When must receipts be submitted?", "policy-travel"),
    ("What is the daily meal allowance?", "policy-travel"),
    ("Where must production credentials be stored?", "policy-security"),
    ("How quickly must P1 incidents be acknowledged?", "policy-incident"),
    ("How long are diagnostic logs kept?", "policy-data"),
]
def main():
    provider=os.getenv("RETRIEVAL_BACKEND","tfidf")
    index=EvidenceIndex(provider=provider)
    for k in [1,3]:
        hit=sum(expected in {p["doc_id"] for p in index.search(q,top_k=k)} for q,expected in CASES)
        print(f"{provider} hit@{k}: {hit}/{len(CASES)} synthetic-policy test cases")
    print("These are manually authored illustrative questions, not real-world benchmark measurements.")
if __name__=="__main__":
    main()
