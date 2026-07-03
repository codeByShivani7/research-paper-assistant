from app.embeddings.sentence_transformer import generate_embedding
from app.vector_store.qdrant_store import upsert_chunks
from uuid import uuid4

text = "The Transformer architecture uses self-attention."

embedding = generate_embedding(text)

result = upsert_chunks([
    {
        "id": str(uuid4()),
        "vector": embedding,
        "payload": {
            "paper_id": "test_paper",
            "page_number": 1,
            "chunk_index": 0,
            "text": text,
        },
    }
])

print(result)