def build_prompt(query: str, retrieved_chunks: list[dict]) -> str:
    context_parts = []

    for item in retrieved_chunks:
        meta = item["metadata"]
        doc = item["document"]

        context_parts.append(
            f"Paper: {meta['paper_name']}\n"
            f"Page: {meta['page_number']}\n"
            f"Section: {meta['section']}\n"
            f"Text: {doc}\n"
        )

    context = "\n" + ("\n---\n".join(context_parts))

    prompt = f"""
You are a research paper assistant.

Answer the user's question only using the provided context.
If the answer is not clearly available in the context, say:
"The answer is not clearly available in the retrieved context."

Also provide concise citations in this format:
(Paper: <paper_name>, Page: <page_number>, Section: <section>)

User Question:
{query}

Retrieved Context:
{context}

Answer:
"""
    return prompt


if __name__ == "__main__":
    sample_query = "What is the main contribution of this paper?"

    sample_chunks = [
        {
            "document": "The paper proposes the Transformer, a model based entirely on attention mechanisms.",
            "metadata": {
                "paper_name": "sample_paper.pdf",
                "page_number": 1,
                "section": "Abstract",
            },
        },
        {
            "document": "The Transformer replaces recurrent layers with multi-headed self-attention.",
            "metadata": {
                "paper_name": "sample_paper.pdf",
                "page_number": 9,
                "section": "Conclusion",
            },
        },
    ]

    prompt = build_prompt(sample_query, sample_chunks)
    print(prompt)