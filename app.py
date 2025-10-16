"""
FinAdvisor API - FastAPI Backend
A REST API for the FinAdvisor chatbot using FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.chatbot import FinAdvisorChatbot
import uvicorn

app = FastAPI(
    title="FinAdvisor API",
    description="Financial Advisor Chatbot API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot
chatbot = FinAdvisorChatbot()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "FinAdvisor API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for the FinAdvisor chatbot

    Args:
        request: ChatRequest containing the user's message

    Returns:
        ChatResponse containing the chatbot's response
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        response = chatbot.generate_answer(request.message)
        return ChatResponse(response=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )