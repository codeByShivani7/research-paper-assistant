import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.chunking.fixed_chunker import chunk_text
from app.embeddings.sentence_transformer import generate_embeddings
from app.parsers.pdf_parser import extract_pages_from_pdf
from app.vector_store.qdrant_store import upsert_chunks


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


async def upload_paper_service(file: UploadFile) -> dict:
    paper_id = str(uuid4())

    original_filename = file.filename
    stored_filename = f"{paper_id}.pdf"
    file_path = UPLOAD_DIR / stored_filename

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

    texts = [chunk["text"] for chunk in all_chunks]

    embeddings = generate_embeddings(texts) if texts else []

    points = []

    for chunk, embedding in zip(all_chunks, embeddings):
        points.append({
            "id": str(uuid4()),
            "vector": embedding,
            "payload": {
                "paper_id": paper_id,
                "original_filename": original_filename,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
            },
        })

    if points:
        upsert_chunks(points)

    return {
        "paper_id": paper_id,
        "filename": original_filename,
        "content_type": file.content_type,
        "saved_path": str(file_path),
        "total_pages": len(pages),
        "total_chunks": len(all_chunks),
        "indexed_chunks": len(points),
        "first_page_preview": pages[0]["text"][:500] if pages else "",
        "first_chunk_preview": all_chunks[0]["text"][:300] if all_chunks else "",
        "message": "File uploaded, parsed, chunked, embedded, and indexed successfully",
    }