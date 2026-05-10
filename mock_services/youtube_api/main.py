from fastapi import FastAPI, Query
import json
import os

app = FastAPI()

# Load dataset

BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "data/videos.json")) as f:   
    Transcripts = json.load(f)


@app.get("/")
def root():
    return {"message": "Youtube API is running"}

@app.get("/videos/search")
def search_videos(q: str = Query(...)):
    results = []

    for video in Transcripts:
        if q.lower() in video["title"].lower():
            results.append(video)

    return {
        "items": [
            {
            "video_id": v["video_id"],
            "title": v["title"],
            "transcript": v["transcript"],
            "channel": v["channel"],
            "url": v["url"]
            }
            for v in results
        ]
    }
            