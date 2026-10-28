from fastapi.testclient import TestClient
from backend.app import app
from backend.model import dataset,predict
client=TestClient(app)
GOOD={"amount_usd":25,"hour_utc":13,"velocity_24h":1,"merchant_risk":0.1,"account_age_days":900,"distance_km":8}
def test_health():assert client.get("/api/health").json()["status"]=="ok"
def test_deterministic_data():
    x,y=dataset(200); xx,yy=dataset(200)
    assert (x==xx).all() and (y==yy).all()
def test_metrics():
    body=client.get("/api/metrics").json()
    assert body["samples"]==6000 and 0<=body["average_precision"]<=1
    assert len(body["important_features"])==6
def test_prediction_contract():
    body=client.post("/api/predict",json=GOOD).json()
    assert 0<=body["risk_score"]<=1
    assert body["risk_band"] in {"LOW","REVIEW","HIGH"}
def test_invalid_input():assert client.post("/api/predict",json={**GOOD,"hour_utc":26}).status_code==422
def test_model_deterministic():assert predict(GOOD)==predict(GOOD)
