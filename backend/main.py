from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Angular Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Metric(BaseModel):
    id: int
    title: str
    status: str
    score: float
    timestamp: str

class ThemeUpdate(BaseModel):
    theme_preference: str

# In-memory seed data
db = {
    "metrics": [
        {"id": 1, "title": "CPU Usage", "status": "stable", "score": 45.5, "timestamp": datetime.now().isoformat()},
        {"id": 2, "title": "Memory Load", "status": "warning", "score": 82.1, "timestamp": datetime.now().isoformat()}
    ],
    "theme": "light"
}

@app.get("/api/health")
def health_check():
    return {"status": "online", "timestamp": datetime.now().isoformat()}

@app.get("/api/analytics", response_model=List[Metric])
def get_analytics():
    return db["metrics"]

@app.post("/api/theme/toggle")
def toggle_theme(payload: ThemeUpdate):
    db["theme"] = payload.theme_preference
    return {"message": "Theme updated successfully", "current_theme": db["theme"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)