# Configuration settings
import os
from dotenv import load_dotenv
load_dotenv()

class Config():
    SOMETHING = 'something'
    YOUTUBE_API = os.environ['YOUTUBE_API']

config = Config()