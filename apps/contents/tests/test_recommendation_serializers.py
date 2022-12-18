from django.utils import timezone

from apps.search.test import TestCase

from ..models import Recommendation
from ..serializers import RecommendationRuleSerializer


class RecommendationRuleSerializerTest(TestCase):
    def setUp(self):
        super().setUp()
        start_datetime = timezone.now() - timezone.timedelta(days=7)
        end_datetime = timezone.now() + timezone.timedelta(days=7)
        self.recommendation = Recommendation(
            id=1,
            prefix_url=""
            "https://example.org/news/\n"
            "https://example.org/products/\n",
            link="https://wwww.google.com/",
            is_active=True,
            title="2022年、年越しライブ",
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        self.recommendation.save()

        self.recommendation_rule = {
            "title": "2022年、年越しライブ",
            "link": "https://wwww.google.com/",
            "publication_period": {
                "gte": start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "lte": end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "is_active": True,
            "query": {
                "bool": {
                    "should": [
                        {
                            "prefix": {
                                "prefix_url": "https://example.org/news/"
                            }
                        },
                        {
                            "prefix": {
                                "prefix_url": "https://example.org/products/"
                            }
                        },
                    ],
                    "minimum_should_match": "1",
                },
            },
        }

    def test_recommendation_rule_serializer(self):
        recommendation_rule = RecommendationRuleSerializer(
            instance=self.recommendation
        ).data
        recommendation_rule.pop("id")
        self.assertEqual(self.recommendation_rule, recommendation_rule)
