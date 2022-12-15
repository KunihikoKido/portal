from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.search.models import BaseSearchModel


class ClassificationType(models.TextChoices):
    CATEGORY = "category", _("Category")
    REGION = "region", _("Region")
    COUNTRY = "country", _("Country")
    CITY = "city", _("City")
    SEASON = "season", _("Season")


class Classification(BaseSearchModel):
    slug = models.SlugField(_("slug"))
    name = models.CharField(_("name"), max_length=100)
    order = models.PositiveIntegerField(
        _("order"),
        default=0,
        blank=False,
        null=False,
    )
    classification_type = models.CharField(
        _("classification type"),
        max_length=20,
        choices=ClassificationType.choices,
        default=ClassificationType.CATEGORY,
    )

    synonyms = models.TextField(
        _("synonyms"),
        blank=True,
        help_text=_(
            "The clause (query) should appear in the matching documents.",
        ),
    )
    antonyms = models.TextField(
        _("antonyms"),
        blank=True,
        help_text=_(
            "The clause (query) must not appear in the matching documents.",
        ),
    )

    class Meta:
        verbose_name = _("Classification")
        verbose_name_plural = _("Classifications")
        ordering = ("order",)
        unique_together = ["slug", "name", "classification_type"]
        index_name = "portal.documents.product"
        mapping_template = "mappings/portal.documents.classification.json"

    def __str__(self):
        return self.name

    def clean_splitlines(self, text):
        return "\n".join([t for t in text.splitlines() if t])

    def save(self, *args, **kwargs):
        self.synonyms = self.clean_splitlines(self.synonyms)
        self.antonyms = self.clean_splitlines(self.antonyms)
        super().save(*args, **kwargs)

    def get_key(self):
        return "≠".join(["%06d" % self.order, self.slug, self.name])

    def get_serialized_classification_rule(self):
        from ..serializers import ClassificationRuleSerializer

        classification_rule = ClassificationRuleSerializer(instance=self).data
        return classification_rule

    def index_classification(self):
        classification_tule = self.get_serialized_classification_rule()
        doc_id = classification_tule.pop("id")
        self._meta.model.index_document(
            id=doc_id,
            document=classification_tule,
        )

    def delete_classification(self):
        classification_tule = self.get_serialized_classification_rule()
        doc_id = classification_tule.pop("id")
        self._meta.model.delete_document(id=doc_id)
