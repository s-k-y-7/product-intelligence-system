from fastapi import FastAPI, Query
import json
import os

app = FastAPI()

# Load dataset
BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "data/products.json")) as f:   
    PRODUCTS = json.load(f)


@app.get("/")
def root():
    return {"message": "Ecommerce API is running"}


@app.get("/products/search")
def search_products(q: str = Query(...)):
    results = []

    for product in PRODUCTS:
        if q.lower() in product["title"].lower():
            results.append(product)
  
    return {
        "items": [
            {
                "title": p["title"],
                "price": p["price"],
                "rating": p["rating"],
                "availability": p["availability"],
                "source_identifier": p["id"]
            }
            for p in results
        ]
    }

    

