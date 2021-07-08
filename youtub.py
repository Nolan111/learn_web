import requests
from bs4 import BeautifulSoup
import json
import requests
import time
import os


def get_video_id(query):
    r = requests.get(
        "https://content-youtube.googleapis.com/youtube/v3/search?maxResults=1&videoDuration=any&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM",
        headers={
            "x-referer": "https://explorer.apis.google.com",
            "x-origin": "https://explorer.apis.google.com",
        },
        params={"q": f"русский трейлер {query}", "type": "trailer"},
    )
    try:
        return r.json()["items"][0]["id"]["videoId"]
    except KeyError:
        return "PkT0PJwy8mI"
