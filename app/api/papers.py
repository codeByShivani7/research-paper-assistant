from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path
from app.services.pdf_parser import extract_pages_from_pdf

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_pages_from_pdf(str(file_path))

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_path": str(file_path),
        "total_pages": len(pages),
        "first_page_preview": pages[0]["text"][:500] if pages else "",
        "message": "File recieved Successfully"
    }