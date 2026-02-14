import requests

print("Testing Interaction API...")
url = "http://localhost:8000/api/v1/interactions"
payload = {
    "user_id": "test_user_123",
    "paper_id": "http://arxiv.org/abs/2602.12172v1", # Use an ID that likely exists or was returned in search
    "interaction_type": "star"
}

try:
    res = requests.post(url, json=payload)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.json()}")
except Exception as e:
    print(f"Error: {e}")
