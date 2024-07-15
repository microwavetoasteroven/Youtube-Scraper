from fastapi import FastAPI
from dotenv import load_dotenv
from app.config import config
load_dotenv()
import os

app = FastAPI()

@app.get("/")
async def root():
    print(config.SOMETHING)
    print(os.environ['MYENV'])
    return {"message": "Hello World"}
