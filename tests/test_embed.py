import pytest
import numpy as np
import os
import json
from unittest.mock import MagicMock, patch
from src.embed_papers import generate_embeddings

@pytest.fixture
def mock_sentence_transformer():
    with patch('src.embed_papers.SentenceTransformer') as MockClass:
        yield MockClass

def test_embedding_generation(mock_sentence_transformer, tmp_path):
    # Setup Data
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    papers_file = data_dir / "papers.json"
    
    papers = [
        {"id": "1", "title": "T1", "abstract": "A1"},
        {"id": "2", "title": "T2", "abstract": "A2"}
    ]
    with open(papers_file, "w") as f:
        json.dump(papers, f)
        
    # Mock Model
    mock_model = mock_sentence_transformer.return_value
    # Mock encode to return random numpy array of shape (2, 384)
    mock_model.encode.return_value = np.random.rand(2, 384).astype(np.float32)
    
    # Run
    generate_embeddings(
        input_file=str(papers_file),
        output_dir=str(data_dir),
        model_name="dummy-model"
    )
    
    # Verify outputs
    embeddings_file = data_dir / "embeddings.npy"
    mapping_file = data_dir / "id_mapping.json"
    
    assert embeddings_file.exists()
    assert mapping_file.exists()
    
    # Check content
    emb = np.load(embeddings_file)
    assert emb.shape == (2, 384)
    
    with open(mapping_file) as f:
        ids = json.load(f)
    assert ids == ["1", "2"]
