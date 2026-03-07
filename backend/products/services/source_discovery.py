from products.models import Product, Source, ProductSource
from django.db import transaction


class SourceDiscoveryService:

    @transaction.atomic
    def discover_sources(self, product: Product):

        if product.status != Product.Status.CREATED:
            raise Exception("Source discovery already executed")

        sources = Source.objects.filter(is_active=True)

        product_sources = []

        for source in sources:

            ps = ProductSource.objects.create(
                product=product,
                source=source,
                url=source.base_url,  # store base_url only
                status=ProductSource.Status.PENDING
            )

            product_sources.append(ps)

        product.status = Product.Status.COLLECTING
        product.save()

        return product_sources