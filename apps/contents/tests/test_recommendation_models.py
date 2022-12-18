from django.utils import timezone

from apps.search.test import TestCase

from ..models import Recommendation


class RecommendationModelTest(TestCase):
    def setUp(self):
        super().setUp()
        start_datetime = timezone.now() - timezone.timedelta(days=7)
        end_datetime = timezone.now() + timezone.timedelta(days=7)
        self.prefix_urls = [
            "https://example.org/news/",
            "https://example.org/products/",
        ]

        self.recommendation = Recommendation(
            id=1,
            prefix_url="\n".join(self.prefix_urls),
            link="https://wwww.google.com/",
            is_active=True,
            title="2022年、年越しライブ",
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        self.recommendation.save()
        self.recommendation.index_recommendation()
        self.recommendation.refresh_index()

    def test_get_prefix_urls(self):
        self.assertEqual(
            self.prefix_urls,
            self.recommendation.get_prefix_urls(),
        )

    def test_search_recommendations(self):
        from ..serializers import RecommendationRuleSerializer

        recommendation = RecommendationRuleSerializer(
            instance=self.recommendation
        ).data
        recommendation.pop("id")
        recommendation.pop("query")

        view_url = "https://example.org/news/0001"
        response = self.recommendation.search(
            query={
                "percolate": {
                    "field": "query",
                    "document": {"prefix_url": view_url},
                }
            },
            source_excludes=["query"],
        )

        self.assertEqual(1, response["hits"]["total"]["value"])
        self.assertEqual(
            recommendation, response["hits"]["hits"][0]["_source"]
        )
