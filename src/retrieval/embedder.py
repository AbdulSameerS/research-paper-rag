import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
import chromadb


def load_chunks(input_path: str) -> list[dict]:
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_vector_store(chunks: list[dict], persist_path: str = "data/index/chroma_db") -> None:
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=persist_path)
    collection = client.get_or_create_collection(name="research_papers")

    documents = [chunk["text"] for chunk in chunks]
    ids = [chunk["chunk_id"] for chunk in chunks]
    metadatas = [
        {
            "paper_id": chunk["paper_id"],
            "paper_name": chunk["paper_name"],
            "page_number": chunk["page_number"],
        }
        for chunk in chunks
    ]

    embeddings = model.encode(documents).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB at {persist_path}")


if __name__ == "__main__":
    input_json = "data/processed/sample_paper_chunks.json"

    chunks = load_chunks(input_json)
    build_vector_store(chunks)