from .model import get_bundle
def main():
    m=get_bundle()["metrics"]
    print("SYNTHETIC DATA — ILLUSTRATIVE DEVELOPMENT METRICS ONLY")
    for field in ["samples","fraud_rate","test_samples","average_precision","roc_auc","baseline_average_precision","threshold","confusion_matrix"]:
        print(f"{field}: {m[field]}")
    print("Threshold was chosen on the same validation split used for the report: do not treat these as unbiased deployment metrics.")
if __name__=="__main__":main()
