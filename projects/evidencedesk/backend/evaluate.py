"""Run offline retrieval checks. Report results from this run; never claim external benchmark scores."""
from .retrieval import EvidenceIndex
CASES = [
    ("When must receipts be submitted?", "policy-travel"),
    ("What is the daily meal allowance?", "policy-travel"),
    ("Where must production credentials be stored?", "policy-security"),
    ("How quickly must P1 incidents be acknowledged?", "policy-incident"),
    ("How long are diagnostic logs kept?", "policy-data"),
]
def main():
    index = EvidenceIndex()
    correct = sum(expected in {p["doc_id"] for p in index.search(q, top_k=3)} for q, expected in CASES)
    print(f"Retrieval hit@3 on {len(CASES)} synthetic policy questions: {correct}/{len(CASES)}")
    print("This is a toy evaluation, not an accuracy claim about real documents.")
if __name__ == "__main__":
    main()
