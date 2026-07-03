from fastapi import APIRouter

from app.services.chat_service import chat

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("")
def ask_question(question: str):
    return chat(question)