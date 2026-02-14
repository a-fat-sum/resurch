import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def generate_embeddings(
    input_file="data/papers.json",
    output_dir="data",
    model_name="sentence-transformers/all-MiniLM-L6-v2", # Starting small for PoC
    batch_size=32
):
    """
    Generates embeddings for papers in the input JSON file.
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run ingestion first.")
        return

    print(f"Loading papers from {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        papers = json.load(f)

    if not papers:
        print("No papers found.")
        return

    # Prepare texts: Title + Abstract
    texts = [f"{p.get('title', '')} [SEP] {p.get('abstract', '')}" for p in papers]
    ids = [p.get('id') for p in papers]

    print(f"Loading model: {model_name}...")
    model = SentenceTransformer(model_name)

    print(f"Generating embeddings for {len(texts)} papers...")
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True)

    # Save embeddings
    os.makedirs(output_dir, exist_ok=True)
    embeddings_file = os.path.join(output_dir, "embeddings.npy")
    np.save(embeddings_file, embeddings)
    
    # Save ID mapping
    mapping_file = os.path.join(output_dir, "id_mapping.json")
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(ids, f, indent=4)

    print(f"Saved embeddings to {embeddings_file} shape: {embeddings.shape}")
    print(f"Saved ID mapping to {mapping_file}")

if __name__ == "__main__":
    generate_embeddings()
