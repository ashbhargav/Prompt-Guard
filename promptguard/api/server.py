from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ..core.detector import PromptGuard, Config

app = FastAPI(title="PromptGuard API", description="API for detecting prompt injection attacks")

# Initialize globally for now (stateless mostly)
guard = PromptGuard()

class AnalyzeRequest(BaseModel):
    prompt: str

class AnalyzeResponse(BaseModel):
    is_suspicious: bool
    risk_score: float
    confidence: float
    detected_patterns: list
    recommendation: str
    explanation: str

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    result = guard.analyze(request.prompt)
    return result

@app.get("/")
async def root():
    return {"status": "online", "message": "PromptGuard API is running"}
