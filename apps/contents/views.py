from rest_framework import viewsets

from .models import Recommendation
from .serializers import RecommendationRuleSerializer


class RecommendationRuleViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationRuleSerializer
