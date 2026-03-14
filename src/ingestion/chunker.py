import json
from pathlib import Path


def split_into_word_chunks(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()

    if not words:
        return []

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]
        if not chunk_words:
            continue
        chunks.append(" ".join(chunk_words))

        if start + chunk_size >= len(words):
            break

    return chunks


def chunk_parsed_pages(parsed_pages: list[dict]) -> list[dict]:
    chunked_records = []

    for page in parsed_pages:
        chunks = split_into_word_chunks(page["text"], chunk_size=300, overlap=50)

        for chunk_index, chunk_text in enumerate(chunks, start=1):
            chunked_records.append(
                {
                    "paper_id": page["paper_id"],
                    "paper_name": page["paper_name"],
                    "page_number": page["page_number"],
                    "chunk_id": f'{page["paper_id"]}_p{page["page_number"]}_c{chunk_index}',
                    "text": chunk_text,
                }
            )

    return chunked_records


def load_parsed_json(input_path: str) -> list[dict]:
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_chunked_output(chunked_records: list[dict], output_path: str) -> None:
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunked_records, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    input_json = "data/processed/sample_paper_parsed.json"
    output_json = "data/processed/sample_paper_chunks.json"

    parsed_pages = load_parsed_json(input_json)
    chunked_records = chunk_parsed_pages(parsed_pages)
    save_chunked_output(chunked_records, output_json)

    print(f"Loaded {len(parsed_pages)} parsed pages.")
    print(f"Created {len(chunked_records)} chunks.")
    print(f"Saved chunked output to {output_json}")