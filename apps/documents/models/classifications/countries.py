import django.db.models.options as model_options
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .classifications import Classification, ClassificationType

model_options.DEFAULT_NAMES += (
    "index_name",
    "mapping_template",
    "elasticsearch",
)

ELASTICSEARCH = settings.ELASTICSEARCH["default"]


class CountryClassificationManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                classification_type=ClassificationType.COUNTRY,
            )
        )


class CountryClassification(Classification):
    objects = CountryClassificationManager()

    class Meta:
        proxy = True
        verbose_name = _("Counrty classification")
        verbose_name_plural = _("Country classifications")
        index_name = "portal.documents.product"
        mapping_template = "mappings/portal.documents.classification.json"
        elasticsearch = ELASTICSEARCH["client"]

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.COUNTRY:
            self.classification_type = ClassificationType.COUNTRY
        super().save(*args, **kwargs)
