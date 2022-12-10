from django.db import models

from .classifications import Classification, ClassificationType


class CityClassificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            classification_type=ClassificationType.CITY)

    def create(self, **kwargs):
        kwargs.update({'classification_type': ClassificationType.CITY})
        return super().create(**kwargs)


class CityClassification(Classification):
    objects = CityClassificationManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.CITY:
            self.classification_type = ClassificationType.CITY
        super().save(*args, **kwargs)
