from app.util.youtube_api import search_videos_by_keyword
from app.util.arxiv import safe_search_arxiv
from app.util.llama_docs import read_my_docs
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.util.neo4j_manager import create_paper
import json
import os
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],  # Add all origins you need
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/youtube_search")
async def youtube_search(keyword: str = Query(default="GraphRag")):
    video_generator = search_videos_by_keyword(keyword=keyword, max_results=1, max_pages=1)
    return StreamingResponse(video_generator, media_type="text/event-stream")

@app.get("/arxiv_search")
async def arxiv_search(query: str = Query(default="quantum computing", description="Query to search for in arXiv")):
    """
    Endpoint to search arXiv and stream results using Server-Sent Events.
    """
    return StreamingResponse(safe_search_arxiv(query), media_type="text/event-stream")

@app.get("/document_loader")
async def document_loader():
    """
    Endpoint to load all documents from data folder
    """
    data = read_my_docs()

    # cleaned_text = re.sub(' +', ' ', ' '.join([dict(x)['text'] for x in data]).replace('\n', ' '))
    print("Current working directory:", os.getcwd())
    # Define the folder path and file name
    folder_path = "./cleaned_data"
    cleaned_text = []
    for item in data:
        file_name = item['title']

    # Define the full path to the file
        file_path = os.path.join(folder_path, file_name)

    # Write the output to the file
        with open(file_path, "w") as file:
            file.write(item['body'])
        cleaned_text.append(item['body'])
        print(f"Output written to {file_path}")

    return cleaned_text

@app.get("/arxiv_search_with_neo4j")
async def arxiv_search_with_neo4j(query: str = Query(default="quantum computing", description="Query to search for in arXiv")):
    """
    Endpoint to search arXiv, insert results into Neo4j, and stream results using Server-Sent Events.
    """
    neo4j_uri = "bolt://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "password"  # Replace with your actual Neo4j password

    async def stream_and_insert():
        for result in safe_search_arxiv(query):
            # Load the JSON result
            paper_details = json.loads(result.split("data: ")[1])
            
            # Insert into Neo4j
            create_paper(
                uri=neo4j_uri,
                user=neo4j_user,
                password=neo4j_password,
                title=paper_details["title"],
                authors=paper_details["authors"],
                abstract=paper_details["abstract"],
                pdf_url=paper_details["pdf_url"],
                published=paper_details["published"],
                updated=paper_details["updated"]
                # keywords and institution are omitted as they are not present in paper_details
            )

            # Yield the result for streaming
            yield result

    return StreamingResponse(stream_and_insert(), media_type="text/event-stream")