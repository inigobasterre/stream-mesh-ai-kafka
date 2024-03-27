import json
import logging
import requests


def fetch_playlist_items_page(api_key, playlist_id, page_token=None):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/playlistItems",
        params={"key": api_key, "playlistId": playlist_id, "part": "contentDetails", "page_token": page_token},
    )
    payload = json.loads(response.text)
    logging.debug("GOT %s", payload)
    return payload

def fetch_playlist_items(api_key, playlist_id, page_token=None):
    payload = fetch_playlist_items_page(api_key, playlist_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token:
        yield from fetch_playlist_items(api_key, playlist_id, next_page_token)

def fetch_video_page(api_key, video_id, page_token=None):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={"key": api_key, "id": video_id, "part": "snippet,statistics", "page_token": page_token},
    )
    payload = json.loads(response.text)
    logging.debug("GOT %s", payload)
    return payload

def fetch_videos(api_key, video_id, page_token=None):
    payload = fetch_video_page(api_key, video_id, page_token)

    yield from payload["items"]

    next_page_token = payload.get("nextPageToken")

    if next_page_token:
        yield from fetch_videos(api_key, video_id, next_page_token)