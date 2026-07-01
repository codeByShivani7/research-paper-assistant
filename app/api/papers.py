from fastapi import APIRouter, UploadFile, File

from app.services.paper_service import upload_paper_service

router = APIRouter()


@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    return await upload_paper_service(file)