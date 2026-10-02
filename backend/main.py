from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="eCommerce Product Data Scraping - MG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductData(BaseModel):
    id: int
    product_url: str
    description: str
    technical_specifications: dict
    extraction_timestamp: str
    status: str

class ScrapeRequest(BaseModel):
    url: str

class ThemeSettings(BaseModel):
    theme: str
    toggle_bg_color: str

# In-memory storage
db = [
    ProductData(id=1, product_url="https://example.com/p1", description="Sample Product", technical_specifications={"weight": "1kg"}, extraction_timestamp=datetime.now().isoformat(), status="completed")
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/scrape/trigger")
def trigger_scrape(request: ScrapeRequest):
    return {"message": "Scraping job initiated", "url": request.url, "job_id": "job_123"}

@app.get("/api/data/export", response_model=List[ProductData])
def get_data():
    return db

@app.patch("/api/settings/theme")
def update_theme(settings: ThemeSettings):
    return {"message": "Theme updated successfully", "settings": settings}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)