from django.db import models
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    url = models.URLField(_('url'), unique=True)
    title = models.CharField(_('title'), blank=True, max_length=100)
    description = models.TextField(_('description'), blank=True)
    image_url = models.URLField(_('image url'), blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title or self.url


class Product(Base):
    product_id = models.CharField(_('product id'), blank=True, max_length=100)
    brand_name = models.CharField(_('brand name'), blank=True, max_length=100)

    offer_count = models.IntegerField(_('offer count'), blank=True, null=True)
    low_price = models.IntegerField(
        _('low price'), blank=True, null=True)
    high_price = models.IntegerField(
        _('high price'), blank=True, null=True)
    price_currency = models.CharField(
        _('price currency'), blank=True, max_length=100)

    rating = models.FloatField(_('review rating'))
    review_count = models.IntegerField(
        _('review count'), blank=True, null=True)
