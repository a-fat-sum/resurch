import pytest
import shutil
import os
import json
from unittest.mock import MagicMock, patch
from src.ingest_arxiv import ingest_arxiv_papers

@pytest.fixture
def mock_arxiv_client():
    with patch('src.ingest_arxiv.arxiv.Client') as MockClient:
        yield MockClient

def test_fetched_structure(mock_arxiv_client, tmp_path):
    # Setup mock
    mock_result = MagicMock()
    mock_result.entry_id = "http://arxiv.org/abs/2101.00001v1"
    mock_result.title = "Test Paper"
    mock_result.summary = "Abstract"
    mock_result.authors = [MagicMock(name="Author")]
    mock_result.published.isoformat.return_value = "2021-01-01"
    mock_result.updated.isoformat.return_value = "2021-01-01"
    mock_result.categories = ["cs.AI"]
    mock_result.pdf_url = "http://pdf"
    
    client_instance = mock_arxiv_client.return_value
    client_instance.results.return_value = [mock_result]
    
    # Run ingestion
    with patch('src.ingest_arxiv.os.makedirs') as mock_dirs, \
         patch('builtins.open', new_callable=MagicMock) as mock_open, \
         patch('json.dump') as mock_json_dump, \
         patch('src.ingest_arxiv.os.path.exists', return_value=False):
         
        ingest_arxiv_papers(max_results=1)
        
        # Verify
        args, _ = mock_json_dump.call_args
        saved_data = args[0]
        assert len(saved_data) == 1
        assert saved_data[0]["title"] == "Test Paper"
        assert saved_data[0]["id"] == "http://arxiv.org/abs/2101.00001v1"

def test_deduplication(mock_arxiv_client, tmp_path):
    # Existing paper
    existing = [{
        "id": "existing_id", 
        "title": "Old Paper",
        "entry_id": "existing_id"
    }]
    
    # Mock return same paper + new one
    mock_res1 = MagicMock()
    mock_res1.entry_id = "existing_id"
    mock_res1.title = "Old Paper"
    mock_res1.authors = []
    mock_res1.published.isoformat.return_value = ""
    mock_res1.updated.isoformat.return_value = ""

    mock_res2 = MagicMock()
    mock_res2.entry_id = "new_id"
    mock_res2.title = "New Paper"
    mock_res2.authors = []
    mock_res2.published.isoformat.return_value = ""
    mock_res2.updated.isoformat.return_value = ""

    client_instance = mock_arxiv_client.return_value
    client_instance.results.return_value = [mock_res1, mock_res2]

    # Run
    with patch('src.ingest_arxiv.os.makedirs'), \
         patch('src.ingest_arxiv.os.path.exists', return_value=True), \
         patch('builtins.open', new_callable=MagicMock) as mock_open, \
         patch('json.load', return_value=existing), \
         patch('json.dump') as mock_dump:
         
        ingest_arxiv_papers(max_results=2)
        
        args, _ = mock_dump.call_args
        final_list = args[0]
        # Should have 2 unique papers, not 3 (existing + existing + new)
        assert len(final_list) == 2
        ids = [p["id"] for p in final_list]
        assert "existing_id" in ids
        assert "new_id" in ids
