from django.db import models

from .classifications import Classification, ClassificationType


class SeasonClassificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            classification_type=ClassificationType.SEASON)


class SeasonClassification(Classification):
    objects = SeasonClassificationManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.SEASON:
            self.classification_type = ClassificationType.SEASON
        super().save(*args, **kwargs)
