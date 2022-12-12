import json

from django.template.loader import render_to_string
from rest_framework import serializers

from ..models import Classification


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = "__all__"


class ClassificationIndexSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    def get_key(self, obj):
        return obj.get_key()

    class Meta:
        model = Classification
        fields = ("slug", "name", "order", "key")


class ClassificationPercolatorSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    query = serializers.SerializerMethodField()
    _meta = serializers.SerializerMethodField()

    class Meta:
        model = Classification
        fields = ["id", "query", "_meta"]

    def get_id(self, obj):
        return "classification-{}".format(obj.id)

    def get_query(self, obj):
        rendered = render_to_string(
            "percolators/classification_query.json",
            {"classification": obj},
        )
        return json.loads(rendered)

    def get__meta(self, obj):
        rendered = render_to_string(
            "percolators/classification_meta.json",
            {"classification": obj},
        )
        return json.loads(rendered)
