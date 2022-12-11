from django.db import models
from django.utils.translation import gettext_lazy as _


class ClassificationType(models.TextChoices):
    CATEGORY = 'category', _('Category')
    REGION = 'region', _('Region')
    COUNTRY = 'country', _('Country')
    CITY = 'city', _('City')
    SEASON = 'season', _('Season')


class Classification(models.Model):
    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), unique=True, max_length=100)
    order = models.PositiveIntegerField(
        _('order'), default=0, blank=False, null=False)
    classification_type = models.CharField(
        _('classification type'), max_length=20,
        choices=ClassificationType.choices,
        default=ClassificationType.CATEGORY)

    synonyms = models.TextField(
        _('synonyms'), blank=True,
        help_text=_('The clause (query) should appear '
                    'in the matching documents.'))
    antonyms = models.TextField(
        _('antonyms'), blank=True,
        help_text=_('The clause (query) must not appear '
                    'in the matching documents.'))

    class Meta:
        verbose_name = _('Classification')
        verbose_name_plural = _('Classifications')
        ordering = ('order',)

    def __str__(self):
        return self.name

    def clean_splitlines(self, text):
        return '\n'.join([t for t in text.splitlines() if t])

    def save(self, *args, **kwargs):
        self.synonyms = self.clean_splitlines(self.synonyms)
        self.antonyms = self.clean_splitlines(self.antonyms)
        super().save(*args, **kwargs)

    def get_key(self):
        return '≠'.join(['%06d' % self.order, self.slug, self.name])
