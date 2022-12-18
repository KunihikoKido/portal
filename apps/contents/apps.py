from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecommendationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.contents"
    verbose_name = _("contents")

    def ready(self):
        from .models import Recommendation

        Recommendation.create_index()
        Recommendation.put_mapping()
