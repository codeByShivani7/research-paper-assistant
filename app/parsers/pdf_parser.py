import fitz

def extract_text_from_pdf(file_path: str) -> str:
    document = fitz.open(file_path)
    text_parts = []

    for page in document:
        text = page.get_text()
        text_parts.append(text)

    document.close()

    return "\n".join(text_parts)

def extract_pages_from_pdf(file_path: str) -> list[dict]:
    document = fitz.open(file_path)
    pages = []
    for page_index, page in enumerate(document):
        pages.append({
            "page_number": page_index + 1,
            "text": page.get_text()
        })
    document.close()
    return pages
