from fastapi import FastAPI, Query
import json
import os

app = FastAPI()

# Load dataset
BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "data/reviews.json")) as f:
    REVIEWS = json.load(f)


@app.get("/")
def root():
    return {"message": "Text Review API is running"}


@app.get("/reviews/search")
def search_reviews(q: str = Query(...)):
    results = []

    for review in REVIEWS:
        if q.lower() in review["title"].lower():
            results.append(review)

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
