from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ClassificationType(models.TextChoices):
    CATEGORY = 'category', _('Category')
    REGION = 'region', _('Region')
    COUNTRY = 'country', _('Country')
    CITY = 'city', _('City')


class Classification(models.Model):
    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), unique=True, max_length=100)
    order = models.PositiveIntegerField(
        _('order'), default=0, blank=False, null=False)
    classification_type = models.CharField(
        _('classification type'), max_length=20,
        choices=ClassificationType.choices,
        default=ClassificationType.CATEGORY)
    language = models.CharField(
        _('language'), max_length=10, choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE)

    synonyms = models.TextField(
        _('synonyms'), blank=True,
        help_text=_('The clause (query) should appear '
                    'in the matching documents.'))
    antonyms = models.TextField(
        _('antonyms'), blank=True,
        help_text=_('The clause (query) must not appear '
                    'in the matching documents.'))

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name
