from googleapiclient.discovery import build
from app.config import config



def yt():
    api_key = config.YOUTUBE_API
    return build('youtube', 'v3', developerKey=api_key)

def search_videos_by_keyword(keyword, max_results=10):
    youtube = yt()
    request = youtube.search().list(
        part="snippet",
        q=keyword,
        maxResults=max_results,
        type="video"
    )
    response = request.execute()

    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        print(f"Video ID: {video_id}, Title: {title}")

# Example usage
search_videos_by_keyword("FastAPI")
