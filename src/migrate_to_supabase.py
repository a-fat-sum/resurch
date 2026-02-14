import os
import json
import numpy as np
from supabase import create_client, Client
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_SERVICE_KEY not found in .env")
    exit(1)

supabase: Client = create_client(url, key)

def migrate_data():
    papers_file = "data/papers.json"
    embeddings_file = "data/embeddings.npy"
    mapping_file = "data/id_mapping.json"

    if not (os.path.exists(papers_file) and os.path.exists(embeddings_file)):
        print("Error: Local data not found.")
        return

    print("Loading local data...")
    with open(papers_file, "r", encoding="utf-8") as f:
        papers = json.load(f)
    
    embeddings = np.load(embeddings_file)
    with open(mapping_file, "r", encoding="utf-8") as f:
        ids = json.load(f)
        
    # Map ID to embedding
    id_to_emb = {id_: emb for id_, emb in zip(ids, embeddings)}

    print(f"Migrating {len(papers)} papers to Supabase...")
    
    batch_size = 50
    batch = []
    
    for paper in tqdm(papers):
        pid = paper["id"]
        if pid not in id_to_emb:
            continue
            
        record = {
            "id": pid,
            "title": paper.get("title"),
            "abstract": paper.get("abstract"),
            "url": paper.get("pdf_url"),
            "authors": paper.get("authors", []),
            "categories": paper.get("categories", []),
            "published": paper.get("published"),
            "embedding": id_to_emb[pid].tolist()
        }
        batch.append(record)
        
        if len(batch) >= batch_size:
            try:
                supabase.table("papers").upsert(batch).execute()
            except Exception as e:
                print(f"Error upserting batch: {e}")
            batch = []

    if batch:
        try:
            supabase.table("papers").upsert(batch).execute()
        except Exception as e:
            print(f"Error upserting final batch: {e}")

    print("Migration complete.")

if __name__ == "__main__":
    migrate_data()
