from fastapi import FastAPI
from app.config import config
import os
from app.util.youtube_api import search_videos_by_keyword
import logging

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/youtube_search/{keyword}/{max_pages}/{results_per_page}")
async def youtube_search(keyword:str, max_pages: int, results_per_page:int):
    # Example of how to use this generator
    result = []
    for video in search_videos_by_keyword(keyword, max_results=results_per_page, max_pages=max_pages):
        print(f"Video ID: {video['video_id']}, Title: {video['title']}")
        result.append(video)

    return {"message": result}
