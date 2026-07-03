def build_rag_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    context = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        payload = chunk["payload"]

        context.append(
            f"""
Source {i}
Filename: {payload["original_filename"]}
Page: {payload["page_number"]}

Content:
{payload["text"]}
"""
        )

    context_text = "\n\n".join(context)

    prompt = f"""
You are an AI research assistant.

Answer ONLY using the information provided in the context.

If the answer is not present in the context, say:

"I couldn't find this information in the uploaded documents."

Do not hallucinate.
Do not make assumptions.

=========================
Context

{context_text}

=========================

Question:

{question}

Answer:
"""

    return prompt