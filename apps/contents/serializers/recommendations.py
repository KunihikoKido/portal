import json

from django.template.loader import render_to_string
from rest_framework import serializers

from ..models import Recommendation


class RecommendationRuleSerializer(serializers.ModelSerializer):
    publication_period = serializers.SerializerMethodField()
    query = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = [
            "id",
            "title",
            "link",
            "publication_period",
            "is_active",
            "query",
        ]

    def get_id(self, obj):
        return str(obj.id)

    def get_publication_period(self, obj):
        return {
            "gte": obj.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "lte": obj.end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def get_query(self, obj):
        rendered = render_to_string(
            "percolators/recommendation_query.json", {"recommendation": obj}
        )
        return json.loads(rendered)
