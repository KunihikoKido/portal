from rest_framework import viewsets

from .models import ProductDocument
from .serializers import ProductDocumentSerializer


class ProductDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProductDocument.objects.all()
    serializer_class = ProductDocumentSerializer
