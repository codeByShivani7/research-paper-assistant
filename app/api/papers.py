from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path
from app.services.pdf_parser import extract_pages_from_pdf
from app.services.chunking import chunk_text

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_pages_from_pdf(str(file_path))

    all_chunks = []

    for page in pages:
        chunks = chunk_text(page["text"])

        for index, chunk in enumerate(chunks):
            all_chunks.append({
                "page_number": page["page_number"],
                "chunk_index": index,
                "text": chunk,
            })

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_path": str(file_path),
        "total_pages": len(pages),
        "first_page_preview": pages[0]["text"][:500] if pages else "",
        "total_chunks": len(all_chunks),
        "first_chunk_preview": all_chunks[0]["text"][:300] if all_chunks else "",
        "message": "File recieved Successfully"
    }