from products.models import Insight


class InsightService:

    def generate(self, product):
        from products.services.processing import ProcessingService

        processed_data = ProcessingService().process_product(product)

        offers = processed_data.get("offers", [])
        pros = processed_data.get("pros", [])
        cons = processed_data.get("cons", [])

        # ---- No offers found ----
        if not offers:
            insight_content = {
                "status": "no_match",
                "message": "No relevant products found",
                "canonical_product": None,
                "best_platform": None,
                "platform_scores": [],
                "pros_summary": pros,
                "cons_summary": cons,
            }

            self._save_insight(product, insight_content)
            return insight_content

        # ---- Price normalization ----
        prices = [o["price"] for o in offers if o.get("price") is not None]

        if prices:
            min_price = min(prices)
            max_price = max(prices)
        else:
            min_price = max_price = None

        platform_scores = []

        for offer in offers:

            price = offer.get("price")
            rating = offer.get("rating")
            availability = offer.get("availability", True)

            # --- Price Score ---
            if price is None or min_price is None:
                price_score = 0.5
            elif max_price == min_price:
                price_score = 1
            else:
                price_score = (max_price - price) / (max_price - min_price)

            # --- Rating Score ---
            rating_score = 0.5 if rating is None else rating / 5

            # --- Relevance Score ---
            # default = 1.0 for sources that don't provide match_score
            relevance_score = offer.get("match_score")

            # --- Final Weighted Score ---
            final_score = (
                0.5 * relevance_score +
                0.3 * price_score +
                0.2 * rating_score
            )

            # --- Availability Penalty ---
            if not availability:
                final_score *= 0.5

            platform_scores.append({
                "platform": offer["platform"],
                "title": offer["title"],
                "price": price,
                "rating": rating,
                "availability": availability,
                "relevance": relevance_score,
                "final_score": round(final_score, 4),
            })

        # ---- Rank offers ----
        platform_scores.sort(key=lambda x: x["final_score"], reverse=True)

        best_offer = platform_scores[0]

        insight_content = {
            "canonical_product": best_offer["title"],
            "best_platform": best_offer["platform"],
            "platform_scores": platform_scores[0],
            "pros_summary": pros,
            "cons_summary": cons,
        }

        self._save_insight(product, insight_content)

        return insight_content

    def _save_insight(self, product, content):

        Insight.objects.update_or_create(
            product=product,
            defaults={"content": content}
        )

        product.status = product.Status.READY
        product.save()