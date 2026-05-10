import requests
from .base import BaseCollector


class LocalEcommerceCollector(BaseCollector):

    def collect(self, product_source):

        # same pattern as your existing collector
        query_words = product_source.product.query.lower().split()
        query_string = " ".join(query_words)

        base_url = product_source.source.base_url
        full_url = f"{base_url}/products/search"

        print("CALLING:", full_url)

        response = requests.get(
            full_url,
            params={"q": query_string},
            timeout=3
        )

        print("DONE:", full_url)

        if response.status_code != 200:
            raise Exception(f"LocalEcommerce fetch failed: {response.status_code}")

        data = response.json()

        items = []

        for product in data.get("items", []):

            title = product.get("title", "").lower()

            # SAME matching logic (consistency is important)
            match_count = sum(1 for word in query_words if word in title)

            if match_count == 0:
                continue

            match_ratio = match_count / len(query_words)

            if match_ratio < 0.7:
                continue

            items.append({
                "title": product.get("title"),
                "price": product.get("price"),
                "currency": "USD",
                "rating": product.get("rating"),
                "availability": product.get("availability"),
                "source_identifier": product.get("source_identifier"),
                "match_score": match_ratio
            })


        return {
            "content": {
                "items": items
            },
            "identifier": full_url,
            "data_type": "JSON"
        }