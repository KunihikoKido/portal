from rest_framework import serializers

from apps.classifications.models import ClassificationType
from apps.classifications.serializers import ClassificationIndexSerializer

from ..models import ProductDocument


class ProductDocumentSerializer(serializers.ModelSerializer):
    category_classifications = serializers.SerializerMethodField()
    region_classifications = serializers.SerializerMethodField()
    country_classifications = serializers.SerializerMethodField()
    city_classifications = serializers.SerializerMethodField()
    season_classifications = serializers.SerializerMethodField()

    def get_category_classifications(self, obj):
        serializer = ClassificationIndexSerializer(
            obj.category_classifications.filter(
                classification_type=ClassificationType.CATEGORY,
            ),
            many=True,
        )
        return serializer.data

    def get_region_classifications(self, obj):
        serializer = ClassificationIndexSerializer(
            obj.region_classifications.filter(
                classification_type=ClassificationType.REGION,
            ),
            many=True,
        )
        return serializer.data

    def get_country_classifications(self, obj):
        serializer = ClassificationIndexSerializer(
            obj.country_classifications.filter(
                classification_type=ClassificationType.COUNTRY,
            ),
            many=True,
        )
        return serializer.data

    def get_city_classifications(self, obj):
        serializer = ClassificationIndexSerializer(
            obj.city_classifications.filter(
                classification_type=ClassificationType.CITY,
            ),
            many=True,
        )
        return serializer.data

    def get_season_classifications(self, obj):
        serializer = ClassificationIndexSerializer(
            obj.season_classifications.filter(
                classification_type=ClassificationType.SEASON,
            ),
            many=True,
        )
        return serializer.data

    class Meta:
        model = ProductDocument
        fields = "__all__"
