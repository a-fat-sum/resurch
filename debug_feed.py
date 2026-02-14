import requests

print("Testing Feed API...")
# Change this to the user_id you used to star papers
user_id = "user_2swm4i8J4jK5l6M7n8o9p0q1r2" 
# Verify your user_id by looking at the interactions table or logs from previous step
# Or just fetch one if unknown
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)
interactions = supabase.table("user_interactions").select("user_id").limit(1).execute()
if interactions.data:
    user_id = interactions.data[0]['user_id']
    print(f"Using user_id: {user_id}")
else:
    print("No interactions found, cannot test feed without stars.")
    exit()

api_url = f"http://localhost:8000/api/v1/feed?user_id={user_id}"
try:
    res = requests.get(api_url)
    print(f"Status: {res.status_code}")
    papers = res.json()
    print(f"Got {len(papers)} recommendations")
    for p in papers[:3]:
        print(f"- {p['title']}")
except Exception as e:
    print(f"Error: {e}")
