from rest_framework import viewsets

from .models import Classification, ProductDocument
from .serializers import (
    ClassificationPercolatorSerializer,
    ClassificationSerializer,
    ProductDocumentSerializer,
)


class ProductDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProductDocument.objects.all()
    serializer_class = ProductDocumentSerializer


class PercolatorViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationPercolatorSerializer


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
