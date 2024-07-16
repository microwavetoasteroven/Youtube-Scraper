import arxiv
import time
import json

def safe_search_arxiv(query, max_results=10, max_attempts=1, delay=1):
    """
    Generator to query arXiv safely with retries and yield formatted SSE results.
    """
    successful = False  # Flag to track if any results were successfully yielded
    for attempt in range(max_attempts):
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            for result in search.results():  # Use results() method here
                successful = True
                paper_details = {
                    "title": result.title,
                    "authors": ", ".join(author.name for author in result.authors),
                    "abstract": result.summary.replace("\n", " "),  # Replace newlines to prevent formatting issues
                    "pdf_url": result.pdf_url,
                    "published": result.published.strftime('%Y-%m-%d'),
                    "updated": result.updated.strftime('%Y-%m-%d')
                }
                # Format for SSE and yield
                yield f"data: {json.dumps(paper_details)}\n\n"
            break  # Exit loop after successfully yielding results
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < max_attempts - 1:
                time.sleep(delay)  # Wait before retrying
    
    if not successful:
        print("Failed to fetch results after several attempts.")

