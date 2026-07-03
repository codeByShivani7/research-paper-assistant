from fastapi import APIRouter
from app.api import chat, health, papers

api_router = APIRouter()

api_router.include_router(
    chat.router
)

api_router.include_router(
    health.router,
    prefix='/health',
    tags=['Health'],
)

api_router.include_router(
    papers.router,
    prefix='/papers',
    tags=['Papers'],
)