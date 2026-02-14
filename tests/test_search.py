import pytest
import numpy as np
import json
import os
import faiss
from unittest.mock import MagicMock, patch
from src.search import search_papers

@pytest.fixture
def mock_model():
    with patch('src.search.SentenceTransformer') as MockModel:
        yield MockModel

def test_search_integration(mock_model, tmp_path):
    # Setup Data
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    papers = [
        {"id": "1", "title": "Paper A", "pdf_url": "http://a", "categories": ["cs.AI"]}, 
        {"id": "2", "title": "Paper B", "pdf_url": "http://b", "categories": ["cs.LG"]}
    ]
    with open(data_dir / "papers.json", "w") as f:
        json.dump(papers, f)
        
    ids = ["1", "2"]
    with open(data_dir / "id_mapping.json", "w") as f:
        json.dump(ids, f)
    
    # Create real embeddings (random)
    embeddings = np.random.rand(2, 384).astype(np.float32)
    # Make sure Paper A (index 0) is closer to the query than Paper B
    # Let's say query vector will be ones.
    # We'll set Paper A embedding to ones, Paper B to zeros.
    embeddings[0] = np.ones(384, dtype=np.float32)
    embeddings[1] = np.zeros(384, dtype=np.float32)
    
    np.save(data_dir / "embeddings.npy", embeddings)
    
    # Setup Mock Model to return a vector of ones
    mock_inst = mock_model.return_value
    mock_inst.encode.return_value = np.ones((1, 384), dtype=np.float32)

    # Run Search
    # Should return Paper A first (distance 0)
    results = search_papers("query", data_dir=str(data_dir), top_k=2)
    
    # Verify
    assert len(results) == 2
    assert results[0]["title"] == "Paper A"
    assert results[1]["title"] == "Paper B"
    
    # Check printed output logic (optional, but function returns list so checking list is enough)
