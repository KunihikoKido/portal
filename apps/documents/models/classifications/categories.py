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


class CategoryClassificationManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(classification_type=ClassificationType.CATEGORY)
        )


class CategoryClassification(Classification):
    objects = CategoryClassificationManager()

    class Meta:
        proxy = True
        verbose_name = _("Category classification")
        verbose_name_plural = _("Category classifications")
        index_name = "portal.documents.product"
        mapping_template = "mappings/portal.documents.classification.json"
        elasticsearch = ELASTICSEARCH["client"]

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.CATEGORY:
            self.classification_type = ClassificationType.CATEGORY
        super().save(*args, **kwargs)
