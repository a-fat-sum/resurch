# Phase 1 Test Specification

## Strategy
Use `pytest` for unit and integration testing. Mock external APIs (arXiv) to ensure tests are deterministic and fast.

## Test Cases

### 1. Ingestion (`tests/test_ingest.py`)
- **`test_fetched_data_structure`**:
    - Mock arXiv client response.
    - specific fields (id, title, abstract) must be present.
    - Verify deduplication logic (insert duplicate ID -> count remains same).
- **`test_save_load_integrity`**:
    - Write mock data to temp file.
    - Read back and verify equivalence.

### 2. Embeddings (`tests/test_embed.py`)
- **`test_embedding_shape`**:
    - Pass dummy text list.
    - Verify output shape matches `(N, 1024)` (for GTE-large) or model dim.
- **`test_incrementality`**:
    - If needed: verify only new papers are embedded (v2 feature, maybe skip for v1).

### 3. Search (`tests/test_search.py`)
- **`test_search_exact_match`**:
    - Index a specific unique sentence.
    - Query that exact sentence.
    - Verify it returns as the top result (distance ~0 or Cosine ~1).
- **`test_index_persistence`**:
    - Save Faiss index.
    - Load Faiss index.
    - Search same query, verify same result.
