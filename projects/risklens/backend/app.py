from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .model import get_bundle,predict

class Transaction(BaseModel):
    amount_usd: float = Field(ge=1,le=5000)
    hour_utc: int = Field(ge=0,le=23)
    velocity_24h: int = Field(ge=0,le=35)
    merchant_risk: float = Field(ge=0,le=1)
    account_age_days: float = Field(ge=1,le=4000)
    distance_km: float = Field(ge=0,le=2000)

app=FastAPI(title="RiskLens Synthetic Fraud ML API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_methods=["GET","POST"],allow_headers=["Content-Type"])

@app.get("/api/health")
def health():return {"status":"ok","dataset":"synthetic","model":"gradient-boosted classifier"}

@app.get("/api/metrics")
def metrics():return get_bundle()["metrics"]

@app.post("/api/predict")
def score(transaction:Transaction):return predict(transaction.model_dump())
