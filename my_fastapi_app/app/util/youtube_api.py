from googleapiclient.discovery import build
from app.config import config
from functools import lru_cache

def yt():
    api_key = config.YOUTUBE_API
    return build('youtube', 'v3', developerKey=api_key)

@lru_cache(maxsize=20)
def search_videos_by_keyword(keyword, max_results=10, max_pages=5):
    youtube = yt()
    next_token = None
    page_count = 0

    while page_count < max_pages:
        request = youtube.search().list(
            part="snippet",
            q=keyword,
            maxResults=max_results,
            pageToken=next_token,
            type="video"
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            # Instead of printing, yield each video as a dictionary
            yield {'video_id': video_id, 'title': title}

        next_token = response.get('nextPageToken')
        if not next_token:
            break  # Exit the loop if there's no more pages

        page_count += 1  # Increment the page count





