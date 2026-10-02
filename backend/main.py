from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Angular Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DashboardItem(BaseModel):
    id: int
    title: str
    status: str
    score: float
    timestamp: str
    category: str
    metadata: dict

seed_data = [
    DashboardItem(id=1, title="System Load", status="Active", score=85.5, timestamp=datetime.now().isoformat(), category="Infrastructure", metadata={"node": "prod-01"}),
    DashboardItem(id=2, title="User Auth", status="Warning", score=42.0, timestamp=datetime.now().isoformat(), category="Security", metadata={"node": "auth-02"})
]

@app.get("/api/v1/dashboard/metrics")
async def get_metrics():
    return {"total_items": len(seed_data), "avg_score": sum(i.score for i in seed_data) / len(seed_data), "status": "healthy"}

@app.get("/api/v1/dashboard/data-feed", response_model=List[DashboardItem])
async def get_data_feed(page: int = 1, limit: int = 10):
    return seed_data

@app.post("/api/v1/dashboard/actions")
async def execute_action(action: dict):
    return {"status": "success", "action_received": action}

@app.get("/api/health")
async def health_check():
    return {"status": "online", "timestamp": datetime.now().isoformat()}
