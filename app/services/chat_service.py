from app.llm.gemini_client import generate_answer
from app.prompts.prompt_builder import build_rag_prompt
from app.services.retrieval_service import retrieve_relevant_chunks


def chat(question: str) -> dict:
    retrieval = retrieve_relevant_chunks(
        question=question,
        top_k=5,
    )

    prompt = build_rag_prompt(
        question=question,
        retrieved_chunks=retrieval["results"],
    )

    answer = generate_answer(prompt)

    sources = []

    seen = set()

    for chunk in retrieval["results"]:
        payload = chunk["payload"]

        key = (
            payload["original_filename"],
            payload["page_number"],
        )

        if key not in seen:
            seen.add(key)

            sources.append(
                {
                    "filename": payload["original_filename"],
                    "page": payload["page_number"],
                }
            )

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }