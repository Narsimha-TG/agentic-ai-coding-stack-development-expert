from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Audiobook TTS & Localization API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NovelTask(BaseModel):
    task_id: str
    novel_title: str
    language_target: str
    voice_profile_id: str
    status: str = "pending"
    progress_percentage: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

# In-memory storage
db = {}

@app.post("/api/v1/process-novel", response_model=NovelTask)
async def process_novel(title: str, lang: str, voice_id: str):
    task_id = str(uuid.uuid4())
    new_task = NovelTask(task_id=task_id, novel_title=title, language_target=lang, voice_profile_id=voice_id)
    db[task_id] = new_task
    return new_task

@app.get("/api/v1/tasks/{task_id}", response_model=NovelTask)
async def get_task(task_id: str):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    return db[task_id]

@app.post("/api/v1/translate")
async def translate_chapter(task_id: str, chapter_index: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Translation triggered for chapter {chapter_index}"}

@app.get("/api/v1/audio/{task_id}/download")
async def download_audio(task_id: str):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"url": f"/static/audio/{task_id}.mp3"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "workers": "active"}
