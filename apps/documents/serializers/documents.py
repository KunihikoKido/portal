from rest_framework import serializers

from ..models import ProductDocument


class ProductDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDocument
        fields = ["url", "title", "description"]
