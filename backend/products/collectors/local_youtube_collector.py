import requests
from .base import BaseCollector


class LocalYoutubeCollector(BaseCollector):

    def collect(self, product_source):
        query_words = product_source.product.query.lower().split()
        query_string = " ".join(query_words)

        base_url = product_source.source.base_url
        full_url = f"{base_url}/videos/search"

        print("CALLING:", full_url)

        response = requests.get(
            full_url,
            params={"q": query_string},
            timeout=3
        )

        print("DONE:", full_url)

        if response.status_code != 200:
            raise Exception(f"LocalYoutube fetch failed: {response.status_code}")

        data = response.json()

        best_video = None
        best_match_ratio = 0

        for video in data.get("items", []):
            title = video.get("title", "").lower()
            match_count = sum(1 for word in query_words if word in title)

            if match_count == 0:
                continue

            match_ratio = match_count / len(query_words)

            if match_ratio < 0.7:
                continue

            if match_ratio > best_match_ratio:
                best_match_ratio = match_ratio
                best_video = video

        if not best_video:
            return {
                "content": "",
                "identifier": full_url,
                "data_type": "TRANSCRIPT"
            }

        return {
            "content": best_video.get("transcript", ""),
            "identifier": best_video.get("url", best_video.get("video_id")),
            "data_type": "TRANSCRIPT"
        }
