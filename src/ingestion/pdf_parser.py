import json
from pathlib import Path
import fitz  # PyMuPDF


def parse_pdf(pdf_path: str) -> list[dict]:
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    paper_id = pdf_file.stem
    paper_name = pdf_file.name

    doc = fitz.open(pdf_file)
    parsed_pages = []

    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        text = page.get_text("text").strip()

        parsed_pages.append(
            {
                "paper_id": paper_id,
                "paper_name": paper_name,
                "page_number": page_index + 1,
                "text": text,
            }
        )

    doc.close()
    return parsed_pages


def save_parsed_output(parsed_pages: list[dict], output_path: str) -> None:
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_pages, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    sample_pdf = "data/raw/sample_paper.pdf"
    output_json = "data/processed/sample_paper_parsed.json"

    parsed = parse_pdf(sample_pdf)
    save_parsed_output(parsed, output_json)

    print(f"Parsed {len(parsed)} pages.")
    print(f"Saved output to {output_json}")