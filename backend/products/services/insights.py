from products.models import Insight, Product
from products.services.processing import ProcessingService
from django.utils import timezone


class InsightService:
    def generate(self, product):

        processing_service = ProcessingService()

        processed = processing_service.process_product(product)

        prices = processed["prices"]
        pros = processed["pros"]
        cons = processed["cons"]

        best_price = prices[0] if prices else None

        insight_content = {
            "best_price": best_price,
            "price_ranking": prices,
            "pros_summary": list(set(pros)),
            "cons_summary": list(set(cons)),
            "generated_at": timezone.now().isoformat(),
        }

        insight, created = Insight.objects.update_or_create(
            product=product,
            defaults={"content": insight_content}
        )

        # FIX: mark pipeline complete
        product.status = Product.Status.READY
        product.save()

        return insight