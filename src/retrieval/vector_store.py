from sentence_transformers import SentenceTransformer
import chromadb


def search_vector_store(query: str, top_k: int = 3, persist_path: str = "data/index/chroma_db"):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=persist_path)
    collection = client.get_collection(name="research_papers")

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results


if __name__ == "__main__":
    sample_query = "What is the main contribution of this paper?"

    results = search_vector_store(sample_query, top_k=3)

    print("Top retrieved chunks:\n")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), start=1):
        print(f"Result {i}")
        print(f"Paper: {meta['paper_name']}")
        print(f"Page: {meta['page_number']}")
        print(f"Distance: {dist}")
        print(f"Text: {doc[:500]}...")
        print("-" * 80)