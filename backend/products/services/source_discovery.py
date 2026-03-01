# class SourceDiscoveryService:

#     def discover_sources(self, product):
#         1. validate product status
#         2. fetch active sources
#         3. determine relevant sources
#         4. create ProductSource entries
#         5. update Product status

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

            url = self.build_source_url(product.query, source)

            ps = ProductSource.objects.create(
                product=product,
                source=source,
                url=url,
                status=ProductSource.Status.PENDING
            )

            product_sources.append(ps)

        product.status = Product.Status.COLLECTING
        product.save()

        return product_sources


    def build_source_url(self, query, source):
        return f"{source.base_url}/search?q={query}"