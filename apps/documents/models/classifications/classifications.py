import django.db.models.options as model_options
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.search.models import BaseSearchModel

model_options.DEFAULT_NAMES += (
    "index_name",
    "mapping_template",
    "elasticsearch",
)

ELASTICSEARCH = settings.ELASTICSEARCH["default"]


class ClassificationType(models.TextChoices):
    CATEGORY = "category", _("Category")
    REGION = "region", _("Region")
    COUNTRY = "country", _("Country")
    CITY = "city", _("City")
    SEASON = "season", _("Season")


class Classification(BaseSearchModel):
    slug = models.SlugField(_("slug"), unique=True)
    name = models.CharField(_("name"), unique=True, max_length=100)
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
        index_name = "portal.documents.product"
        mapping_template = "mappings/portal.documents.classification.json"
        elasticsearch = ELASTICSEARCH["client"]

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

    def index_classification(self):
        from ...serializers import ClassificationPercolatorSerializer

        percolator = ClassificationPercolatorSerializer(instance=self).data
        doc_id = percolator.pop("id")
        self._meta.model.index_document(
            id=doc_id,
            document=percolator,
        )
