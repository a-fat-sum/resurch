import arxiv
import json
import os
from datetime import datetime, timezone

def ingest_arxiv_papers(query="cat:cs.AI OR cat:cs.LG OR cat:cs.CV", max_results=100):
    """
    Fetches papers from arXiv based on the query and saves them to a JSON file.
    """
    print(f"Fetching {max_results} papers for query: {query}...")
    
    # Construct the default client
    client = arxiv.Client()
    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    papers = []
    # Use the client to iterate over results
    for result in client.results(search):
        paper_data = {
            "id": result.entry_id,
            "title": result.title,
            "abstract": result.summary,
            "authors": [author.name for author in result.authors],
            "published": result.published.isoformat(),
            "updated": result.updated.isoformat(),
            "categories": result.categories,
            "pdf_url": result.pdf_url,
            "entry_id": result.entry_id
        }
        papers.append(paper_data)

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "papers.json")

    # Load existing papers if file exists to append/update
    existing_papers = []
    if os.path.exists(output_file):
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                existing_papers = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {output_file} is corrupted or empty. Overwriting.")
            existing_papers = []

    # Create a dict of existing papers for easy lookup/deduplication
    existing_dict = {p["id"]: p for p in existing_papers}
            
    # Update/Add new papers
    for p in papers:
        existing_dict[p["id"]] = p
        
    final_papers = list(existing_dict.values())
    print(f"Total papers: {len(final_papers)} (New: {len(final_papers) - len(existing_papers)})")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_papers, f, indent=4, ensure_ascii=False)

    print(f"Saved papers to {output_file}")

if __name__ == "__main__":
    ingest_arxiv_papers()
