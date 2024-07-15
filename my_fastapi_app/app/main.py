from fastapi import FastAPI
from app.config import config
import os

app = FastAPI()

@app.get("/")
async def root():
    print(config.SOMETHING)
    print(os.environ['YOUTUBE_API'])
    return {"message": "Hello World"}
