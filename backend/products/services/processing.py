from products.models import RawData


class ProcessingService:

    def process_product(self, product):

        raw_data_qs = RawData.objects.filter(
            product_source__product=product,
            status=RawData.Status.FETCHED
        ).select_related("product_source__source")

        offers = []
        pros = []
        cons = []
        review_texts = []

        for raw in raw_data_qs:

            source_type = raw.product_source.source.type

            if source_type == "ECOMMERCE":

                offer_list = self.extract_best_offer(raw)

                if offer_list:
                    offers.extend(offer_list)

            elif source_type in ["VIDEO", "REVIEW"]:

                review_texts.append(raw.content)

                p, c = self.extract_pros_cons(raw.content)

                pros.extend(p)
                cons.extend(c)

        return {
            "offers": offers,
            "pros": pros,
            "cons": cons,
            "review_texts": review_texts,
        }

    def extract_best_offer(self, raw):

        if raw.data_type != "json":
            return None

        import json

        data = raw.content

        if isinstance(data, str):
            data = json.loads(data)
            
        items = data.get("items", [])

        if not items:
            return None

        # Choose best item
        # Priority:
        # 1. Highest match_score (if exists)
        # 2. Lowest price

        def sort_key(item):
            return (
                -item.get("match_score", 1),  # default 1 if not present
                item.get("price", float("inf"))
            )

        items.sort(key=sort_key)

        top_items = items[:3]   # keep top 3 candidates per source

        offers = []

        for item in top_items:
            offers.append({
                "platform": raw.product_source.source.name,
                "title": item.get("title"),
                "price": item.get("price"),
                "rating": item.get("rating"),
                "availability": item.get("availability"),
                "identifier": item.get("source_identifier"),
                "match_score": item.get("match_score", 1.0)
            })

        return offers

    def extract_pros_cons(self, text):

        pros = []
        cons = []

        text_lower = text.lower()

        if "good" in text_lower or "excellent" in text_lower:
            pros.append("positive feedback detected")

        if "bad" in text_lower or "poor" in text_lower:
            cons.append("negative feedback detected")

        return pros, cons