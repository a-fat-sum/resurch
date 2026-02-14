import os
import requests
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Check Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

try:
    count = supabase.table("papers").select("*", count="exact", head=True).execute()
    print(f"Total papers in DB: {count.count}")
except Exception as e:
    print(f"Error checking DB: {e}")

# Test Search API
try:
    print("\nTesting Search API...")
    res = requests.get("http://localhost:8000/api/v1/search?q=learning&limit=5")
    print(f"Status: {res.status_code}")
    print(f"Response: {res.json()}")
except Exception as e:
    print(f"Error testing API: {e}")
