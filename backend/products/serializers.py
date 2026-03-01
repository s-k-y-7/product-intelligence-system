#serializers are used to convert python + database and json back and forth, so that frontend and backend can communicate with each other. They are the mordern replacement for forms in django (but they offer more than just form functionality...).

from rest_framework import serializers
from .models import Product, Insight

class ProductSerializer(serializers.ModelSerializer):

    insight = serializers.SerializerMethodField()


    class Meta:

        model = Product

        fields = [
            "id",
            "query",
            "status",
            "created_at",
            "updated_at",
            "insight",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "insight",
        ]


    def get_insight(self, obj):

        try:

            return obj.insight.content

        except Insight.DoesNotExist:

            return None