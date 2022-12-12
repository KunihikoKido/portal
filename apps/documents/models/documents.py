import json

import django.db.models.options as model_options
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..models import (
    CategoryClassification,
    CityClassification,
    CountryClassification,
    RegionClassification,
    SeasonClassification,
)
from .classifications import ClassificationType

model_options.DEFAULT_NAMES += (
    "index_name",
    "mapping_template",
    "elasticsearch",
)

ELASTICSEARCH = settings.ELASTICSEARCH["default"]


class BaseDocument(models.Model):
    url = models.URLField(_("url"), unique=True)
    title = models.CharField(_("title"), blank=True, max_length=100)
    description = models.TextField(_("description"), blank=True)
    image_url = models.URLField(_("image url"), blank=True)
    pub_date = models.DateTimeField(
        verbose_name=_("publication date"), default=timezone.now, db_index=True
    )

    is_active = models.BooleanField(_("active"), default=False)

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
            index=cls._meta.index_name, ignore=[400, 404]
        )

    @classmethod
    def delete_index(cls):
        return cls._meta.elasticsearch.indices.delete(
            index=cls._meta.index_name, ignore=[400, 404]
        )

    @classmethod
    def exists_index(cls):
        return cls._meta.elasticsearch.indices.exists(
            index=cls._meta.index_name,
        )

    @classmethod
    def put_mapping(cls):
        templates = json.loads(render_to_string(cls._meta.mapping_template))
        return cls._meta.elasticsearch.indices.put_mapping(
            index=cls._meta.index_name, **templates
        )

    @classmethod
    def flush_index(cls):
        return cls._meta.elasticsearch.indices.flush(
            index=cls._meta.index_name,
        )

    @classmethod
    def refresh_index(cls):
        return cls._meta.elasticsearch.indices.refresh(
            index=cls._meta.index_name,
        )

    @classmethod
    def search(cls, query=None, **kwargs):
        return cls._meta.elasticsearch.search(
            index=cls._meta.index_name, query=query, **kwargs
        )

    @classmethod
    def index_document(cls, id, document, **kwargs):
        return cls._meta.elasticsearch.index(
            index=cls._meta.index_name, id=id, document=document, **kwargs
        )

    @classmethod
    def get_document(cls, id, **kwargs):
        return cls._meta.elasticsearch.get(
            index=cls._meta.index_name,
            id=id,
            **kwargs,
        )

    @classmethod
    def delete_document(cls, id, **kwargs):
        return cls._meta.elasticsearch.delete(
            index=cls._meta.index_name, id=id, **kwargs
        )


class ProductDocument(BaseDocument):
    product_id = models.CharField(_("product id"), blank=True, max_length=100)
    brand_name = models.CharField(_("brand name"), blank=True, max_length=100)

    offer_count = models.IntegerField(_("offer count"), blank=True, null=True)
    low_price = models.IntegerField(_("low price"), blank=True, null=True)
    high_price = models.IntegerField(_("high price"), blank=True, null=True)
    price_currency = models.CharField(
        _("price currency"),
        blank=True,
        max_length=100,
    )

    rating = models.FloatField(
        _("review rating"),
        default=0.0,
        blank=False,
        null=False,
    )
    review_count = models.PositiveIntegerField(
        _("review count"), default=0, blank=False, null=False
    )

    category_classifications = models.ManyToManyField(
        "documents.CategoryClassification",
        verbose_name=_("category classifications"),
        blank=True,
        related_name="CategoryProductDocument",
        limit_choices_to={"classification_type": ClassificationType.CATEGORY},
    )

    region_classifications = models.ManyToManyField(
        "documents.RegionClassification",
        verbose_name=_("region classifications"),
        blank=True,
        related_name="RegionProductDocument",
        limit_choices_to={"classification_type": ClassificationType.REGION},
    )

    country_classifications = models.ManyToManyField(
        "documents.CountryClassification",
        verbose_name=_("country classifications"),
        blank=True,
        related_name="CountryProductDocument",
        limit_choices_to={"classification_type": ClassificationType.COUNTRY},
    )

    city_classifications = models.ManyToManyField(
        "documents.CityClassification",
        verbose_name=_("city classifications"),
        blank=True,
        related_name="CityProductDocument",
        limit_choices_to={"classification_type": ClassificationType.CITY},
    )

    season_classifications = models.ManyToManyField(
        "documents.SeasonClassification",
        verbose_name=_("season classifications"),
        blank=True,
        related_name="SeasonProductDocument",
        limit_choices_to={"classification_type": ClassificationType.SEASON},
    )

    class Meta:
        verbose_name = _("Product document")
        verbose_name_plural = _("Product documents")
        index_name = "portal.documents.product"
        mapping_template = "mappings/portal.documents.product.json"
        elasticsearch = ELASTICSEARCH["client"]

    def clear_classifications(self):
        self.category_classifications.clear()
        self.region_classifications.clear()
        self.country_classifications.clear()
        self.city_classifications.clear()
        self.season_classifications.clear()

    def classify(self):
        from ..serializers import ProductDocumentSerializer

        document = ProductDocumentSerializer(instance=self).data
        response = self._meta.model.search(
            query={
                "percolate": {
                    "field": "query",
                    "document": document,
                },
            }
        )
        self.category_classifications.clear()
        for item in response["hits"]["hits"]:
            source = item["_source"]["_meta"]["classification"]
            classification_type = source["classification_type"]
            slug = source["slug"]
            if classification_type == ClassificationType.CATEGORY:
                classification = CategoryClassification.objects.get(
                    slug=slug,
                )
                self.category_classifications.add(classification)

            elif classification_type == ClassificationType.REGION:
                classification = RegionClassification.objects.get(
                    slug=slug,
                )
                self.region_classifications.add(classification)

            elif classification_type == ClassificationType.COUNTRY:
                classification = CountryClassification.objects.get(
                    slug=slug,
                )
                self.country_classifications.add(classification)

            elif classification_type == ClassificationType.CITY:
                classification = CityClassification.objects.get(
                    slug=slug,
                )
                self.city_classifications.add(classification)

            elif classification_type == ClassificationType.SEASON:
                classification = SeasonClassification.objects.get(
                    slug=slug,
                )
                self.season_classifications.add(classification)
