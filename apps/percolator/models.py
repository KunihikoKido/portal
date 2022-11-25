from django.db import models
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), unique=True, max_length=100)
    order = models.PositiveIntegerField(
        _('order'), default=0, blank=False, null=False)

    class Meta:
        abstract = True
        ordering = ('order',)

    def __str__(self):
        return self.name


class Purpose(Base):
    class Meta(Base.Meta):
        verbose_name = _('purpose')
        verbose_name_plural = _('purposes')


class Experience(Base):
    class Meta(Base.Meta):
        verbose_name = _('experience')
        verbose_name_plural = _('experiences')


class Place(Base):
    class Meta(Base.Meta):
        verbose_name = _('place')
        verbose_name_plural = _('places')


class City(Base):
    class Meta(Base.Meta):
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class Country(Base):
    class Meta(Base.Meta):
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class Region(Base):
    class Meta(Base.Meta):
        verbose_name = _('region')
        verbose_name_plural = _('regions')


class Promotion(Base):
    class Meta(Base.Meta):
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')
