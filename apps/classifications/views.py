from rest_framework import viewsets

from .models import Classification
from .serializers import ClassificationRuleSerializer, ClassificationSerializer


class ClassificationRuleViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationRuleSerializer


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
