from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(status=Product.Status.CREATED)

