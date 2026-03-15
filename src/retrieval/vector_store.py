from sentence_transformers import SentenceTransformer
import chromadb


SECTION_PRIORITY = {
    "Abstract": 0,
    "Conclusion": 1,
    "Introduction": 2,
    "Results": 3,
    "Methods": 4,
    "Experiments": 5,
    "Background": 6,
    "Related Work": 7,
    "Unknown": 8,
    "References": 9,
}


def search_vector_store(query: str, top_k: int = 5, persist_path: str = "data/index/chroma_db"):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path=persist_path)
    collection = client.get_collection(name="research_papers")

    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    combined = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        section = meta.get("section", "Unknown")
        priority = SECTION_PRIORITY.get(section, 8)

        combined.append(
            {
                "document": doc,
                "metadata": meta,
                "distance": dist,
                "section_priority": priority,
            }
        )

    combined.sort(key=lambda x: (x["section_priority"], x["distance"]))
    return combined[:3]


if __name__ == "__main__":
    sample_query = "What is the main contribution of this paper?"

    results = search_vector_store(sample_query, top_k=5)

    print("Top retrieved chunks after reranking:\n")

    for i, item in enumerate(results, start=1):
        meta = item["metadata"]
        doc = item["document"]
        dist = item["distance"]

        print(f"Result {i}")
        print(f"Paper: {meta['paper_name']}")
        print(f"Page: {meta['page_number']}")
        print(f"Section: {meta['section']}")
        print(f"Distance: {dist}")
        print(f"Text: {doc[:500]}...")
        print("-" * 80)