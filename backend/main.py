from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI(title="WEB-SRM Certified POS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
transactions = []
theme_settings = {"background_color": "#ffffff", "accent_color": "#000000"}

class Transaction(BaseModel):
    transaction_id: str
    total_amount: float
    tax_details: Dict[str, float]
    timestamp: str = None

class SRMRequest(BaseModel):
    data: Dict[str, Any]

@app.post("/api/v1/srm/sign")
def sign_transaction(req: SRMRequest):
    return {"srm_signature": f"SRM-SIG-{hash(str(req.data))}", "status": "signed"}

@app.post("/api/v1/transactions")
def create_transaction(tx: Transaction):
    tx.timestamp = datetime.utcnow().isoformat()
    transactions.append(tx.dict())
    return {"message": "Transaction processed", "id": tx.transaction_id}

@app.get("/api/v1/reports/daily")
def get_daily_report():
    return {"date": datetime.utcnow().date(), "total_sales": sum(t['total_amount'] for t in transactions)}

@app.patch("/api/v1/ui/theme")
def update_theme(config: Dict[str, str]):
    theme_settings.update(config)
    return {"message": "Theme updated", "theme": theme_settings}