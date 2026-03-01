from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status as drf_status

from products.models import Product
from products.serializers import ProductSerializer
from products.services.source_discovery import SourceDiscoveryService
from products.services.data_collection import DataCollectionService
from products.services.insights import InsightService



class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


    def perform_create(self, serializer):

        serializer.save(status=Product.Status.CREATED)


    @action(detail=True, methods=["post"])
    def discover(self, request, pk=None):

        product = self.get_object()

        if product.status != Product.Status.CREATED:

            return Response(
                {"error": "Discovery already executed or invalid state"},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        service = SourceDiscoveryService()

        service.discover_sources(product)

        return Response(
            {"message": "Source discovery completed"},
            status=drf_status.HTTP_200_OK
        )
    

    @action(detail=True, methods=["post"])
    def collect(self, request, pk=None):

        product = self.get_object()

        pending_sources = product.sources.filter(
            status="PENDING"
        )

        if not pending_sources.exists():

            return Response(
                {"error": "No pending sources to collect"},
                status=400
            )

        service = DataCollectionService()

        for ps in pending_sources:

            service.collect(ps)

        return Response(
            {"message": "Data collection completed"}
        )   
    
    @action(detail=True, methods=["post"])
    def analyze(self, request, pk=None):

        product = self.get_object()

        service = InsightService()

        insight = service.generate(product)

        return Response(insight.content)