from django.db import models
from django.utils.translation import gettext_lazy as _

from .classifications import Classification, ClassificationType


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
        verbose_name = _("Counrty classification")
        verbose_name_plural = _("Country classifications")
        proxy = True

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.COUNTRY:
            self.classification_type = ClassificationType.COUNTRY
        super().save(*args, **kwargs)
