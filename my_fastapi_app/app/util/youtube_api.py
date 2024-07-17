from googleapiclient.discovery import build
from app.config import config
import json
import os
import datetime

def yt():
    api_key = config.YOUTUBE_API
    return build('youtube', 'v3', developerKey=api_key)

def search_videos_by_keyword(keyword, max_results=1, max_pages=1):
    youtube = yt()  # Retrieve the configured YouTube client
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
        file_name = f"{datetime.datetime.now():%Y%m%d_%H%M%S}_{keyword}.txt"
        folder_path = "./youtube_search"

    # Define the full path to the file
        file_path = os.path.join(folder_path, file_name)

    # Write the output to the file
        with open(file_path, "w") as file:
            file.write(json.dumps(response))
        print(f"Output written to {file_path}")

        for item in response['items']:
            video_info = {
                "video_id": item['id']['videoId'],
                "title": item['snippet']['title'],
                "description": item['snippet']['description']
            }
            # Yield a properly formatted JSON string using json.dumps
            yield f"data: {json.dumps(video_info)}\n\n"

        next_token = response.get('nextPageToken')
        if not next_token:
            break  # Exit the loop if there's no more pages
        page_count += 1
