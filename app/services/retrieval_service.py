from app.embeddings.sentence_transformer import generate_embedding
from app.vector_store.qdrant_store import search_chunks


def retrieve_relevant_chunks(question: str, top_k: int = 5) -> dict:
    query_vector = generate_embedding(question)

    results = search_chunks(
        query_vector=query_vector,
        limit=top_k,
    )

    return {
        "question": question,
        "top_k": top_k,
        "results": results,
    }