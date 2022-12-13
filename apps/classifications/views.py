from rest_framework import viewsets

from .models import Classification
from .serializers import (
    ClassificationPercolatorSerializer,
    ClassificationSerializer,
)


class PercolatorViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationPercolatorSerializer


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
