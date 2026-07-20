import pickle
import os
import requests
from dotenv import load_dotenv
load_dotenv()
YOUTUBE = os.getenv("YOUTUBE_TOKEN")
print("YOUTUBE KEY:", YOUTUBE)
def search_youtube(query, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
    "part": "snippet",
    "q": query,
    "type": "video",
    "maxResults": max_results,
    "key": YOUTUBE
}
    
    response = requests.get(    
    url,
    params=params
)
    data = response.json()
    videos = []

    for video in data["items"]:
        title = video["snippet"]["title"]
        channel = video["snippet"]["channelTitle"]
        thumbnail = video["snippet"]["thumbnails"].get("high", video["snippet"]["thumbnails"]["default"])["url"]
        video_id = video["id"]["videoId"]

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        videos.append({
            "title":title,
            "channel_name":channel,
            "thumbnail":thumbnail,
         # "video_id":video_id,
            "youtube_url":youtube_url
    })

    
    return videos