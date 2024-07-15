from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

def search_videos_by_keyword(keyword, max_results=10):
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
