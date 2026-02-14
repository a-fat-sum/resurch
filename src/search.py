import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import argparse

def search_papers(query, data_dir="data", top_k=5, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Searches for papers semantically similar to the query.
    """
    # Paths
    embeddings_file = os.path.join(data_dir, "embeddings.npy")
    mapping_file = os.path.join(data_dir, "id_mapping.json")
    papers_file = os.path.join(data_dir, "papers.json")

    # Load Data
    if not (os.path.exists(embeddings_file) and os.path.exists(mapping_file) and os.path.exists(papers_file)):
        print("Error: Missing data files. Run ingestion and embedding first.")
        return []

    embeddings = np.load(embeddings_file)
    with open(mapping_file, "r", encoding="utf-8") as f:
        paper_ids = json.load(f)
    with open(papers_file, "r", encoding="utf-8") as f:
        papers_list = json.load(f)
        papers_dict = {p["id"]: p for p in papers_list}

    # Initialize Index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Encode Query
    model = SentenceTransformer(model_name)
    query_vector = model.encode([query], convert_to_numpy=True)

    # Search
    distances, indices = index.search(query_vector, top_k)

    results = []
    print(f"\nResults for '{query}':\n" + "-"*40)
    for i, idx in enumerate(indices[0]):
        if idx < len(paper_ids):
            pid = paper_ids[idx]
            paper = papers_dict.get(pid)
            if paper:
                results.append(paper)
                print(f"{i+1}. [{distances[0][i]:.4f}] {paper['title']}")
                print(f"   {paper['pdf_url']}")
                print(f"   Categories: {', '.join(paper.get('categories', []))}")
                print()
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search papers semantically.")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--top_k", type=int, default=5, help="Number of results")
    args = parser.parse_args()
    
    search_papers(args.query, top_k=args.top_k)
