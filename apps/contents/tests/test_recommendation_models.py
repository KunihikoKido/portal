from django.utils import timezone

from apps.search.test import TestCase

from ..models import Recommendation


class RecommendationModelTest(TestCase):
    def setUp(self):
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
        return super().setUp()

    def test_get_prefix_urls(self):
        self.assertEqual(
            self.prefix_urls,
            self.recommendation.get_prefix_urls(),
        )
