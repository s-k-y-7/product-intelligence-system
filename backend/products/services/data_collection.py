from products.models import ProductSource, RawData
from django.db import transaction


class DataCollectionService:
    @transaction.atomic
    def collect(self, product_source: ProductSource):

        # 1. validate status
        if product_source.status != ProductSource.Status.PENDING:
            raise Exception("Data collection already done or invalid state")

        try:

            # 2. fetch content (mock for now)
            content, identifier, data_type = self.fetch(product_source)

            # 3. create RawData entry
            RawData.objects.create(
                product_source=product_source,
                source_identifier=identifier,
                data_type=data_type,
                content=content,
                status=RawData.Status.FETCHED,
            )

            # 4. update ProductSource status
            product_source.status = ProductSource.Status.COLLECTED
            product_source.save()

        except Exception:

            product_source.status = ProductSource.Status.FAILED
            product_source.save()

            raise


    def fetch(self, product_source: ProductSource):
        """
        Mock fetch logic
        Later this will call real collectors
        """

        query = product_source.product.query

        content = f"Mock data collected for '{query}' from {product_source.source.name}"

        identifier = f"mock-{product_source.id}"

        data_type = RawData.DataType.TEXT

        return content, identifier, data_type