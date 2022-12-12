from django.db import models
from django.utils.translation import gettext_lazy as _

from .classifications import Classification, ClassificationType


class SeasonClassificationManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                classification_type=ClassificationType.SEASON,
            )
        )


class SeasonClassification(Classification):
    objects = SeasonClassificationManager()

    class Meta:
        verbose_name = _("Season classification")
        verbose_name_plural = _("Season classifications")
        proxy = True

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.SEASON:
            self.classification_type = ClassificationType.SEASON
        super().save(*args, **kwargs)
