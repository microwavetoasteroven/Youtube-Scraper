from app.util.youtube_api import search_videos_by_keyword
from app.util.arxiv import safe_search_arxiv
from starlette.responses import StreamingResponse
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from starlette.templating import Jinja2Templates
import time


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}

from fastapi import FastAPI
from starlette.responses import StreamingResponse
import time

app = FastAPI()

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")


def stream_data():
    for i in range(100):
        yield f"data: {i}\n\n"
        time.sleep(1)  # simulate delay

@app.get("/stream")
async def stream():
    return StreamingResponse(stream_data(), media_type="text/event-stream")


# @app.get("/youtube_search/{keyword}/{max_pages}/{results_per_page}")
# async def youtube_search(keyword:str, max_pages: int, results_per_page:int):
#     # Example of how to use this generator
#     result = []
#     for video in search_videos_by_keyword(keyword, max_results=results_per_page, max_pages=max_pages):
#         print(f"Video ID: {video['video_id']}, Title: {video['title']}")
#         result.append(video)
#         yield result

#     # return {"message": result}

# @app.get("/youtube_search/{keyword}/{max_pages}/{results_per_page}")
# async def youtube_search(keyword: str, max_pages: int, results_per_page: int):
#     video_generator = search_videos_by_keyword(keyword, max_results=results_per_page, max_pages=max_pages)
#     return StreamingResponse(video_generator, media_type="text/plain")

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