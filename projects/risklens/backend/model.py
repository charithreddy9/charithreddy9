"""Synthetic fraud-risk classification demo, not a real fraud-detection product."""
from __future__ import annotations
import numpy as np
from functools import lru_cache
from sklearn.datasets import make_classification
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FIELDS = ["amount_usd","hour_utc","velocity_24h","merchant_risk","account_age_days","distance_km"]
LABELS = ["Amount (USD)","Hour (UTC)","24h transaction count","Merchant risk (0–1)","Account age (days)","Distance (km)"]

def dataset(n=6000, seed=19):
    """Deterministic synthetic transaction table. Injected patterns are invented, not observed."""
    rng=np.random.default_rng(seed)
    amount=np.clip(rng.lognormal(4.1,1.0,n),1,5000)
    hour=rng.integers(0,24,n)
    velocity=np.clip(rng.poisson(2.5,n),0,35)
    merchant=rng.beta(2,5,n)
    age=np.clip(rng.exponential(550,n),1,4000)
    distance=np.clip(rng.exponential(50,n),0,2000)
    x=np.column_stack([amount,hour,velocity,merchant,age,distance])
    score=(-5.8 + 1.15*(amount>400) + .95*(velocity>=5) + 2.8*merchant
       + .8*(age<45) + .8*(distance>230) + .6*((hour<=4)|(hour>=23)))
    p=1/(1+np.exp(-score))
    y=rng.binomial(1,p)
    return x,y

@lru_cache(maxsize=1)
def get_bundle():
    x,y=dataset()
    xt,xv,yt,yv=train_test_split(x,y,test_size=.25,random_state=42,stratify=y)
    baseline=Pipeline([("scale",StandardScaler()),("model",LogisticRegression(max_iter=1000,class_weight="balanced",random_state=42))])
    baseline.fit(xt,yt)
    model=HistGradientBoostingClassifier(max_iter=130,learning_rate=.06,l2_regularization=1,random_state=42)
    model.fit(xt,yt)
    scores=model.predict_proba(xv)[:,1]
    precision,recall,thresholds=precision_recall_curve(yv,scores)
    valid=np.where(precision[:-1]>=.70)[0]
    # Threshold selected on validation for illustration; evaluation is optimistic.
    threshold=float(thresholds[valid[np.argmax(recall[:-1][valid])]]) if len(valid) else .5
    predicted=scores>=threshold
    importance=permutation_importance(model,xv,yv,n_repeats=3,random_state=42,scoring="average_precision")
    features=sorted([{"feature":LABELS[i],"importance":round(float(max(0,v)),4)} for i,v in enumerate(importance.importances_mean)],key=lambda z:-z["importance"])
    return {"model":model,"threshold":threshold,"metrics":{
        "samples":len(y),"fraud_rate":round(float(y.mean()),4),
        "test_samples":len(yv),"average_precision":round(float(average_precision_score(yv,scores)),4),
        "roc_auc":round(float(roc_auc_score(yv,scores)),4),
        "baseline_average_precision":round(float(average_precision_score(yv,baseline.predict_proba(xv)[:,1])),4),
        "threshold":round(threshold,4),
        "confusion_matrix":confusion_matrix(yv,predicted,labels=[0,1]).tolist(),
        "important_features":features,
    }}
def predict(transaction):
    values=[float(transaction[name]) for name in FIELDS]
    bundle=get_bundle()
    score=float(bundle["model"].predict_proba(np.array([values]))[0,1])
    return {"risk_score":round(score,4),"risk_band":"HIGH" if score>=bundle["threshold"] else "REVIEW" if score>=.15 else "LOW",
            "flagged":score>=bundle["threshold"],"threshold":round(bundle["threshold"],4),
            "notice":"Model trained on synthetic transactions; not suitable for actual fraud decisions."}
