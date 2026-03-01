from products.models import RawData

class ProcessingService:
    def process_product(self, product):

        raw_data_qs = RawData.objects.filter(
            product_source__product=product,
            status=RawData.Status.FETCHED
        ).select_related("product_source__source") #Fetch all successfully collected RawData for this product, and also fetch their ProductSource and Source efficiently in the same query.

        prices = []
        pros = []
        cons = []
        review_texts = []

        for raw in raw_data_qs:

            source_type = raw.product_source.source.type

            if source_type == "ECOMMERCE":

                price_info = self.extract_price(raw)

                if price_info:
                    prices.append(price_info)

            elif source_type in ["VIDEO", "REVIEW"]:

                review_texts.append(raw.content)

                p, c = self.extract_pros_cons(raw.content)

                pros.extend(p)
                cons.extend(c)

        prices.sort(key=lambda x: x["price"])

        return {
            "prices": prices,
            "pros": pros,
            "cons": cons,
            "review_texts": review_texts,
        }


    def extract_price(self, raw):

        # MOCK extraction for now

        import random

        return {
            "platform": raw.product_source.source.name,
            "price": random.randint(50000, 80000),
            "identifier": raw.source_identifier
        }


    def extract_pros_cons(self, text):

        # MOCK extraction for now

        pros = []
        cons = []

        text_lower = text.lower()

        if "good" in text_lower or "excellent" in text_lower:
            pros.append("positive feedback detected")

        if "bad" in text_lower or "poor" in text_lower:
            cons.append("negative feedback detected")

        return pros, cons