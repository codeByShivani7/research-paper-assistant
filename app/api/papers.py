from fastapi import APIRouter, UploadFile, File

from app.services.paper_service import upload_paper_service
from app.services.retrieval_service import retrieve_relevant_chunks

router = APIRouter()


@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    return await upload_paper_service(file)

@router.get("/search")
def search_papers(question: str, top_k: int = 5):
    return retrieve_relevant_chunks(
        question=question,
        top_k=top_k,
    )