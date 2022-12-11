from django.db import models
from django.utils.translation import gettext_lazy as _

from .classifications import Classification, ClassificationType


class RegionClassificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            classification_type=ClassificationType.REGION)


class RegionClassification(Classification):
    objects = RegionClassificationManager()

    class Meta:
        verbose_name = _('Region classification')
        verbose_name_plural = _('Region classifications')
        proxy = True

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.REGION:
            self.classification_type = ClassificationType.REGION
        super().save(*args, **kwargs)
