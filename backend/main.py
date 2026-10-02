from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Cloud Verification CMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int
    title: str
    status: str
    score: float
    timestamp: str

# In-memory seed data
db = [
    {"id": 1, "title": "Cloud Node Alpha", "status": "active", "score": 98.5, "timestamp": datetime.utcnow().isoformat()},
    {"id": 2, "title": "Cloud Node Beta", "status": "pending", "score": 82.0, "timestamp": datetime.utcnow().isoformat()}
]

@app.get("/api/health")
def health_check():
    return {"status": "online", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_nodes": len(db), "avg_score": sum(r['score'] for r in db) / len(db) if db else 0}

@app.post("/api/reviews", response_model=Review)
def create_review(review: Review):
    db.append(review.dict())
    return review

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)