from celery import shared_task
from products.models import Product
from products.services.source_discovery import SourceDiscoveryService
from products.services.data_collection import DataCollectionService
from products.services.insights import InsightService

@shared_task
def run_pipeline(product_id):
    """
    Runs the complete product intelligence pipeline asynchronously.
    """
    try:
        product = Product.objects.get(id=product_id)
        
        # 1. Discover Sources
        discovery = SourceDiscoveryService()
        discovery.discover_sources(product)
        
        # 2. Collect Data
        collection = DataCollectionService()
        collection.collect(product)
        
        # 3. Analyze and Generate Insight
        insight_service = InsightService()
        insight_service.generate(product)
        
    except Exception as e:
        # If any unexpected error occurs, mark product as FAILED
        # (Though individual services should handle their own failures gracefully)
        print(f"Pipeline failed for product {product_id}: {e}")
        try:
            product = Product.objects.get(id=product_id)
            product.status = Product.Status.FAILED
            product.save()
        except Product.DoesNotExist:
            pass
