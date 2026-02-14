# Phase 1 Implementation Plan: Local Proof-of-Concept

## Goal
Build a local Proof-of-Concept (PoC) for "resurch" that ingests arXiv papers, generates embeddings, and enables semantic search.

## Architecture

### Data Ingestion
- **Source**: arXiv API (via `arxiv` Python package).
- **Categories**: `cs.AI`, `cs.LG`, `cs.CV`.
- **Storage**: JSON file (`data/papers.json`) containing metadata (title, abstract, authors, date, url).
- **Update Mechanism**: Incremental updates (deduplication by arXiv ID).

### Embedding Generation
- **Model**: `thenlper/gte-large` (or similar high-performance transformer).
- **Library**: `sentence-transformers`.
- **Input**: Concatenation of `title + " [SEP] " + abstract`.
- **Storage**: NumPy array (`data/embeddings.npy`) and mapping file (`data/id_mapping.json`).

### Search Interface
- **Engine**: `faiss-cpu` (FlatIndex or IVFFlat for PoC).
- **Interface**: CLI script (`src/search.py`).
- **Query**: Natural language input -> Embedding -> Nearest Neighbor Search.

## Logic Flow
1. `src/ingest_arxiv.py`:
    - Checks `data/papers.json` for existing IDs.
    - Queries arXiv API for new papers.
    - Appends valid unique papers to `data/papers.json`.
2. `src/embed_papers.py`:
    - Loads `data/papers.json`.
    - Checks if embeddings already exist/matches count.
    - Computes embeddings for chunks of papers.
    - Saves `data/embeddings.npy`.
3. `src/search.py`:
    - Loads index/embeddings and paper metadata.
    - Embeds user query.
    - Returns top-k results with formatted output.

## Directory Structure
```
resurch/
├── data/               # Git-ignored data
│   ├── papers.json
│   └── embeddings.npy
├── spec/               # Specifications
│   ├── phase1_implementation_plan.md
│   └── phase1_test_spec.md
├── src/
│   ├── __init__.py
│   ├── ingest_arxiv.py
│   ├── embed_papers.py
│   └── search.py
├── tests/
│   ├── __init__.py
│   ├── test_ingest.py
│   └── test_search.py
├── requirements.txt
└── .gitignore
```
