import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from promptguard import PromptGuard

app = FastAPI()
guard = PromptGuard()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # 1. Validate input first
    security_check = guard.analyze(request.message)
    
    if security_check["recommendation"] == "BLOCK":
        # Log the attack attempt here
        print(f"Blocked attack attempt: {security_check}")
        raise HTTPException(
            status_code=400, 
            detail="I cannot process that request for security reasons."
        )
    
    # 2. Proceed with LLM logic (mocked here)
    return {
        "response": f"Echo: {request.message}", 
        "security_check": "Passed"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
