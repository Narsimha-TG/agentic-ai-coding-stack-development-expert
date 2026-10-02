from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Print-Ready Small Box Design API")

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
data_store = [
    {"id": 1, "title": "Box Design A", "status": "pending", "score": 85.5, "timestamp": datetime.now().isoformat()},
    {"id": 2, "title": "Box Design B", "status": "approved", "score": 92.0, "timestamp": datetime.now().isoformat()}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/analytics")
def get_analytics():
    return {"total_items": len(data_store), "average_score": sum(d['score'] for d in data_store) / len(data_store)}

@app.post("/api/reviews", response_model=Review)
def create_review(review: Review):
    data_store.append(review.dict())
    return review

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)