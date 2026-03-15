import requests

from src.retrieval.vector_store import search_vector_store
from src.generation.prompt_builder import build_prompt


def generate_answer(query: str) -> str:
    retrieved_chunks = search_vector_store(query, top_k=5)
    prompt = build_prompt(query, retrieved_chunks)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()
    data = response.json()
    return data["response"]


if __name__ == "__main__":
    sample_query = "What is the main contribution of this paper?"
    answer = generate_answer(sample_query)

    print("\nGenerated Answer:\n")
    print(answer)