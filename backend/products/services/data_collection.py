from products.models import ProductSource, RawData
from products.collectors.factory import CollectorFactory
from django.db import transaction


class DataCollectionService:

    # @transaction.atomic
    def collect(self, product):

        product_sources = ProductSource.objects.filter(
            product=product,
            status=ProductSource.Status.PENDING
        )
        
        for product_source in product_sources:

            try:
                print("START SOURCE:", product_source.source.code)

                collector = CollectorFactory.get_collector(
                    product_source.source.code
                )


                data = collector.collect(product_source)

                print("END SOURCE:", product_source.source.code)

                from django.db import transaction

                with transaction.atomic():
                    RawData.objects.create(

                        product_source=product_source,

                        content=data["content"],

                        source_identifier=data["identifier"],

                        data_type=data["data_type"],

                        status=RawData.Status.FETCHED

                    )

                    product_source.status = ProductSource.Status.COLLECTED


            except Exception as e:

                product_source.status = ProductSource.Status.FAILED

                print(
                    f"Collection failed for {product_source.id}: {e}"
                )


            product_source.save()