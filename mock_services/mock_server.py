"""
Unified Mock Server
===================
Combines all 4 mock APIs into a single FastAPI application.

Run with:
    uvicorn mock_server:app --port 8050 --reload

Endpoints:
    /ecommerce1/products/search?q=...
    /ecommerce2/products/search?q=...
    /youtube/videos/search?q=...
    /reviews/reviews/search?q=...
"""

from fastapi import FastAPI, Query
import json
import os

BASE_DIR = os.path.dirname(__file__)

# ── Load all datasets ─────────────────────────────────────────────

with open(os.path.join(BASE_DIR, "ecommerce_api/data/products.json")) as f:
    ECOMMERCE_1_PRODUCTS = json.load(f)

with open(os.path.join(BASE_DIR, "ecommerce_api2/data/products.json")) as f:
    ECOMMERCE_2_PRODUCTS = json.load(f)

with open(os.path.join(BASE_DIR, "youtube_api/data/videos.json")) as f:
    YOUTUBE_VIDEOS = json.load(f)

with open(os.path.join(BASE_DIR, "text_review_api/data/reviews.json")) as f:
    TEXT_REVIEWS = json.load(f)


# ── App ───────────────────────────────────────────────────────────

app = FastAPI(title="Product Intelligence — Unified Mock Server")


@app.get("/")
def root():
    return {
        "message": "Unified Mock Server is running",
        "endpoints": [
            "/ecommerce1/products/search?q=...",
            "/ecommerce2/products/search?q=...",
            "/youtube/videos/search?q=...",
            "/reviews/reviews/search?q=...",
        ],
    }


# ── Ecommerce 1 ──────────────────────────────────────────────────

@app.get("/ecommerce1/products/search")
def ecommerce1_search(q: str = Query(...)):
    results = [p for p in ECOMMERCE_1_PRODUCTS if q.lower() in p["title"].lower()]
    return {
        "items": [
            {
                "title": p["title"],
                "price": p["price"],
                "rating": p["rating"],
                "availability": p["availability"],
                "source_identifier": p["id"],
            }
            for p in results
        ]
    }


# ── Ecommerce 2 ──────────────────────────────────────────────────

@app.get("/ecommerce2/products/search")
def ecommerce2_search(q: str = Query(...)):
    results = [p for p in ECOMMERCE_2_PRODUCTS if q.lower() in p["title"].lower()]
    return {
        "items": [
            {
                "title": p["title"],
                "price": p["price"],
                "rating": p["rating"],
                "availability": p["availability"],
                "source_identifier": p["id"],
            }
            for p in results
        ]
    }


# ── YouTube ───────────────────────────────────────────────────────

@app.get("/youtube/videos/search")
def youtube_search(q: str = Query(...)):
    results = [v for v in YOUTUBE_VIDEOS if q.lower() in v["title"].lower()]
    return {
        "items": [
            {
                "video_id": v["video_id"],
                "title": v["title"],
                "transcript": v["transcript"],
                "channel": v["channel"],
                "url": v["url"],
            }
            for v in results
        ]
    }


# ── Text Reviews ─────────────────────────────────────────────────

@app.get("/reviews/reviews/search")
def reviews_search(q: str = Query(...)):
    results = [r for r in TEXT_REVIEWS if q.lower() in r["title"].lower()]
    return {
        "items": [
            {
                "title": r["title"],
                "review_text": r["review_text"],
                "rating": r["rating"],
                "source_identifier": r["id"],
            }
            for r in results
        ]
    }
