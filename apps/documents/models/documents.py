import json

import django.db.models.options as model_options
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .classifications import ClassificationType

model_options.DEFAULT_NAMES += (
    'index_name',
    'mapping_template',
    'elasticsearch'
)

ELASTICSEARCH = settings.ELASTICSEARCH['default']


class BaseDocument(models.Model):
    url = models.URLField(_('url'), unique=True)
    title = models.CharField(_('title'), blank=True, max_length=100)
    description = models.TextField(_('description'), blank=True)
    image_url = models.URLField(_('image url'), blank=True)
    pub_date = models.DateTimeField(
        verbose_name=_("publication date"),
        default=timezone.now, db_index=True)

    is_active = models.BooleanField(_('active'), default=False)

    class Meta:
        abstract = True
        index_name = None
        mapping_template = None
        elasticsearch = None

    def __str__(self):
        return self.title or self.url

    @classmethod
    def create_index(cls):
        return cls._meta.elasticsearch.indices.create(
            index=cls._meta.index_name, ignore=[400, 404])

    @classmethod
    def delete_index(cls):
        return cls._meta.elasticsearch.delete(
            index=cls._meta.index_name, ignore=[400, 404])

    @classmethod
    def exists_index(cls):
        return cls._meta.elasticsearch.exists(
            index=cls._meta.index_name)

    @classmethod
    def put_mapping(cls):
        params = json.loads(render_to_string(cls._meta.mapping_template))
        return cls._meta.elasticsearch.indices.put_mapping(
            index=cls._meta.index_name, **params)

    @classmethod
    def flush(cls):
        return cls._meta.elasticsearch.indices.flush(
            index=cls._meta.index_name)

    @classmethod
    def refresh(cls):
        return cls._meta.elasticsearch.indices.refresh(
            index=cls._meta.index_name)

    @classmethod
    def search(cls, params={}):
        return cls._meta.client.search(**params)


class ProductDocument(BaseDocument):
    product_id = models.CharField(_('product id'), blank=True, max_length=100)
    brand_name = models.CharField(_('brand name'), blank=True, max_length=100)

    offer_count = models.IntegerField(_('offer count'), blank=True, null=True)
    low_price = models.IntegerField(
        _('low price'), blank=True, null=True)
    high_price = models.IntegerField(
        _('high price'), blank=True, null=True)
    price_currency = models.CharField(
        _('price currency'), blank=True, max_length=100)

    rating = models.FloatField(
        _('review rating'), default=0.0, blank=False, null=False)
    review_count = models.PositiveIntegerField(
        _('review count'), default=0, blank=False, null=False)

    category_classifications = models.ManyToManyField(
        'documents.Classification',
        verbose_name=_('category classifications'),
        blank=True,
        related_name='CategoryProductDocument',
        limit_choices_to={'classification_type': ClassificationType.CATEGORY},
    )

    region_classifications = models.ManyToManyField(
        'documents.Classification',
        verbose_name=_('region classifications'),
        blank=True,
        related_name='RegionProductDocument',
        limit_choices_to={'classification_type': ClassificationType.REGION},
    )

    country_classifications = models.ManyToManyField(
        'documents.Classification',
        verbose_name=_('country classifications'),
        blank=True,
        related_name='CountryProductDocument',
        limit_choices_to={'classification_type': ClassificationType.COUNTRY},
    )

    city_classifications = models.ManyToManyField(
        'documents.Classification',
        verbose_name=_('city classifications'),
        blank=True,
        related_name='CityProductDocument',
        limit_choices_to={'classification_type': ClassificationType.CITY},
    )

    class Meta:
        index_name = 'portal.documents.product'
        mapping_template = 'mappings/portal.documents.product.json'
        elasticsearch = ELASTICSEARCH['client']
