# Research Paper RAG

A citation-grounded Retrieval-Augmented Generation (RAG) system for research paper question answering and comparison.

## Project Goal

This project allows users to upload research papers and ask questions such as:

- What is the main contribution of this paper?
- What datasets and metrics were used?
- Compare Paper A vs Paper B
- Give answers with source citations

## Planned Features

- PDF parsing and metadata extraction
- Section-aware chunking
- Dense retrieval with embeddings
- BM25 keyword retrieval
- Hybrid search
- Reranking
- Citation-grounded answer generation
- Evaluation pipeline

## Project Structure

```text
research-paper-rag/
│
├── app/
├── data/
│   ├── raw/
│   ├── processed/
│   └── index/
├── src/
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   └── utils/
├── notebooks/
├── tests/
├── .gitignore
├── README.md
├── requirements.txt
