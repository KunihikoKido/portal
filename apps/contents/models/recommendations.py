from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseContent


class Recommendation(BaseContent):
    title = models.CharField(_("title"), max_length=50)
    link = models.URLField(_("link"), max_length=200)
    start_datetime = models.DateTimeField(
        _("start datetime"), auto_now=False, auto_now_add=False
    )
    end_datetime = models.DateTimeField(
        _("end datetime"), auto_now=False, auto_now_add=False
    )

    class Meta:
        verbose_name = _("recommendation")
        verbose_name_plural = _("recommendations")
        index_name = "portal.contents.recommendations"
        mapping_template = "mappings/portal.contents.recommendation.json"

    def __str__(self):
        return self.title

    def clean_splitlines(self, text):
        return sorted(list(set([t for t in text.splitlines() if t])))

    def get_prefix_urls(self):
        prefix_urls = self.clean_splitlines(self.prefix_url)
        return prefix_urls

    def get_serialized_recommendation(self):
        from ..serializers import RecommendationRuleSerializer

        recommendation_rule = RecommendationRuleSerializer(instance=self).data
        return recommendation_rule

    def index_recommendation(self):
        recommendation = self.get_serialized_recommendation()
        doc_id = recommendation.pop("id")
        self._meta.model.index_document(id=doc_id, document=recommendation)

    def delete_recommendation(self):
        self._meta.model.delete_document(id=self.id)
