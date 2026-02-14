import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys

# We need to mock 'supabase' before importing main because it connects on import
with patch('api.main.create_client') as MockClient:
    from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Resurch API is running"}

@patch('api.main.supabase')
def test_search_endpoint(mock_supabase):
    # Mock Supabase RPC
    mock_response = MagicMock()
    mock_response.data = [{"id": "1", "title": "Test Paper", "abstract": "...", "similarity": 0.9}]
    mock_supabase.rpc.return_value.execute.return_value = mock_response

    # We also need to mock SentenceTransformer which is imported INSIDE the function
    with patch('sentence_transformers.SentenceTransformer') as MockModel:
        mock_model_inst = MockModel.return_value
        mock_model_inst.encode.return_value.tolist.return_value = [0.1, 0.2]
        
        response = client.get("/api/v1/search?q=test")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Paper"

@patch('api.main.supabase')
def test_interaction_endpoint(mock_supabase):
    # Mock Insert
    mock_response = MagicMock()
    mock_response.data = [{"id": "uuid", "status": "created"}]
    mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response
    
    payload = {
        "user_id": "user_123",
        "paper_id": "paper_abc",
        "interaction_type": "star"
    }
    response = client.post("/api/v1/interactions", json=payload)
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
