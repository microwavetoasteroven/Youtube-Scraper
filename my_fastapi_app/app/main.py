from app.util.youtube_api import search_videos_by_keyword
from app.util.arxiv import safe_search_arxiv
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/youtube_search")
async def youtube_search(keyword: str = Query(default="GraphRag")):
    video_generator = search_videos_by_keyword(keyword=keyword, max_results=10, max_pages=5)
    return StreamingResponse(video_generator, media_type="text/event-stream")

@app.get("/arxiv_search")
async def arxiv_search(query: str = Query(default="quantum computing", description="Query to search for in arXiv")):
    """
    Endpoint to search arXiv and stream results using Server-Sent Events.
    """
    return StreamingResponse(safe_search_arxiv(query), media_type="text/event-stream")