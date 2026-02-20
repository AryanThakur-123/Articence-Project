from app.llm.handler import LLMHandler
from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat(message: str):
    return {"response": LLMHandler.process_user_message(message)}
