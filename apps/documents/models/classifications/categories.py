from django.db import models

from .classifications import Classification, ClassificationType


class CategoryClassificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            classification_type=ClassificationType.CATEGORY)


class CategoryClassification(Classification):
    objects = CategoryClassificationManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.classification_type is not ClassificationType.CATEGORY:
            self.classification_type = ClassificationType.CATEGORY
        super().save(*args, **kwargs)
