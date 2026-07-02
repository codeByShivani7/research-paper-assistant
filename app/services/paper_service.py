import shutil
from pathlib import Path

from fastapi import UploadFile

from app.chunking.fixed_chunker import chunk_text
from app.parsers.pdf_parser import extract_pages_from_pdf


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


async def upload_paper_service(file: UploadFile) -> dict:
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
        "total_chunks": len(all_chunks),
        "first_page_preview": pages[0]["text"][:500] if pages else "",
        "first_chunk_preview": all_chunks[0]["text"][:300] if all_chunks else "",
        "message": "File uploaded, parsed, and chunked successfully",
    }