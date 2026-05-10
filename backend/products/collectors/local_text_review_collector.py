import requests
from .base import BaseCollector


class LocalTextReviewCollector(BaseCollector):

    def collect(self, product_source):
        query_words = product_source.product.query.lower().split()
        query_string = " ".join(query_words)

        base_url = product_source.source.base_url
        full_url = f"{base_url}/reviews/search"

        print("CALLING:", full_url)

        response = requests.get(
            full_url,
            params={"q": query_string},
            timeout=3
        )

        print("DONE:", full_url)

        if response.status_code != 200:
            raise Exception(f"LocalTextReview fetch failed: {response.status_code}")

        data = response.json()

        best_review = None
        best_match_ratio = 0

        for review in data.get("items", []):
            title = review.get("title", "").lower()
            match_count = sum(1 for word in query_words if word in title)

            if match_count == 0:
                continue

            match_ratio = match_count / len(query_words)

            if match_ratio < 0.7:
                continue

            if match_ratio > best_match_ratio:
                best_match_ratio = match_ratio
                best_review = review

        if not best_review:
            return {
                "content": "",
                "identifier": full_url,
                "data_type": "TEXT"
            }

        return {
            "content": best_review.get("review_text", ""),
            "identifier": best_review.get("source_identifier", full_url),
            "data_type": "TEXT"
        }
