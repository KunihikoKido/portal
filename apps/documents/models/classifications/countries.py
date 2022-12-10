from django.db import models

from .classifications import Classification, ClassificationType


class CountryClassificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            classification_type=ClassificationType.COUNTRY)


class CountryClassification(Classification):
    objects = CountryClassificationManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.COUNTRY:
            self.classification_type = ClassificationType.COUNTRY
        super().save(*args, **kwargs)
