import requests
from .base import BaseCollector


class DummyJsonCollector(BaseCollector):
    def collect(self, product_source):

        query = product_source.product.query.replace(" ", "+")
        base_url = product_source.source.base_url

        full_url = f"{base_url}/products/search?q={query}"

        print("CALLING:", full_url)

        response = requests.get(full_url, timeout=3)

        print("DONE:", full_url)

        if response.status_code != 200:
            raise Exception(f"DummyJSON fetch failed: {response.status_code}")

        data = response.json()

        items = []

        def compute_match_score(query, title):
            query_words = query.lower().split()
            title_words = title.lower().split()

            matches = sum(1 for w in query_words if w in title_words)

            return matches / len(query_words) if query_words else 0
        
        for product in data.get("products", []):
            match_score = compute_match_score(product_source.product.query, product.get("title", ""))
            if match_score < 0.7:
                continue
            items.append({
                "title": product.get("title"),
                "price": product.get("price"),
                "currency": "USD",  # DummyJSON default
                "rating": product.get("rating"),
                "availability": product.get("stock", 0) > 0,
                "source_identifier": product.get("id"),
                "match_score": match_score
            })
            
        return {
            "content": {
                "items": items
            },
            "identifier": full_url,
            "data_type": "json"
        }