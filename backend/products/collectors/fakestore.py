import requests
from .base import BaseCollector


class FakeStoreCollector(BaseCollector):

    def collect(self, product_source):
        query = product_source.product.query.lower().split()
        base_url = product_source.source.base_url

        full_url = f"{base_url}/products"

        print("CALLING:", full_url)

        response = requests.get(full_url, timeout=3)

        print("DONE:", full_url)

        if response.status_code != 200:
            raise Exception(f"FakeStore fetch failed: {response.status_code}")

        data = response.json()

        items = []

        for product in data:

            title = product.get("title", "").lower()

            # Word-based matching
            match_count = sum(1 for word in query if word in title)

            if match_count == 0:
                continue

            match_ratio = match_count / len(query)

            # Only keep reasonably relevant matches
            if match_ratio < 0.7:
                continue

            items.append({
                "title": product.get("title"),
                "price": product.get("price"),
                "currency": "USD",
                "rating": product.get("rating", {}).get("rate"),
                "availability": True,  # FakeStore doesn't give stock info
                "source_identifier": product.get("id"),
                "match_score": match_ratio
            })

        return {
            "content": {
                "items": items
            },
            "identifier": full_url,
            "data_type": "json"
        }