import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all. In prod, lock this down.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

# --- Models ---
class Paper(BaseModel):
    id: str
    title: str
    abstract: str
    url: Optional[str] = None
    similarity: Optional[float] = None

class UserInteraction(BaseModel):
    user_id: str
    paper_id: str
    interaction_type: str

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Resurch API is running"}

# Load model globally for better performance and to avoid file access issues
from fastembed import TextEmbedding
# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("Loading FastEmbed model...")
model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

@app.get("/api/v1/search", response_model=List[Paper])
def search_papers(q: str, limit: int = 10):
    """
    Semantic search using Supabase pgvector RPC function `match_papers`.
    """
    try:
        # Generate embedding
        # FastEmbed returns a generator, so we take the first item
        vector = list(model.embed([q]))[0].tolist()
        
        # Call RPC
        response = supabase.rpc(
            "match_papers",
            {"query_embedding": vector, "match_threshold": 0.1, "match_count": limit}
        ).execute()
        
        return response.data

    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/interactions")
def record_interaction(interaction: UserInteraction):
    try:
        data = {
            "user_id": interaction.user_id,
            "paper_id": interaction.paper_id,
            "interaction_type": interaction.interaction_type
        }
        response = supabase.table("user_interactions").insert(data).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import numpy as np
import json

@app.get("/api/v1/feed", response_model=List[Paper])
def get_feed(user_id: str):
    """
    Personalized feed based on user's starred papers (centroid method).
    """
    try:
        # 1. Fetch user's starred papers
        interactions = supabase.table("user_interactions").select("paper_id").eq("user_id", user_id).eq("interaction_type", "star").execute()
        starred_ids = [i['paper_id'] for i in interactions.data]

        if not starred_ids:
            return []

        # 2. Fetch embeddings for these papers
        # Note: pgvector returns vectors as strings usually, we need to parse them if so.
        # But supabase-py might parse JSON. Let's be safe.
        response = supabase.table("papers").select("embedding").in_("id", starred_ids).execute()
        
        embeddings = []
        for row in response.data:
            emb = row['embedding']
            if isinstance(emb, str):
                embeddings.append(json.loads(emb))
            else:
                embeddings.append(emb)

        if not embeddings:
            return []

        # 3. Calculate Mean Embedding (User Profile)
        mean_embedding = np.mean(embeddings, axis=0).tolist()

        # 4. Search using this mean embedding
        response = supabase.rpc(
            "match_papers",
            {"query_embedding": mean_embedding, "match_threshold": 0.1, "match_count": 50}
        ).execute()

        # 5. Filter out papers already starred
        recommendations = []
        for paper in response.data:
            if paper['id'] not in starred_ids:
                recommendations.append(paper)
                if len(recommendations) >= 10:
                    break
        
        return recommendations

    except Exception as e:
        print(f"Feed error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
