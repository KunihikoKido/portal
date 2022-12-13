from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.classifications.models import (
    CategoryClassification,
    CityClassification,
    ClassificationType,
    CountryClassification,
    RegionClassification,
    SeasonClassification,
)
from apps.search.models import BaseSearchModel


class BaseDocument(BaseSearchModel):
    url = models.URLField(_("url"), unique=True)
    title = models.CharField(_("title"), blank=True, max_length=100)
    description = models.TextField(_("description"), blank=True)
    image_url = models.URLField(_("image url"), blank=True)
    pub_date = models.DateTimeField(
        verbose_name=_("publication date"),
        default=timezone.now,
        db_index=True,
    )

    is_active = models.BooleanField(_("active"), default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title or self.url


class ProductDocument(BaseDocument):
    product_id = models.CharField(_("product id"), blank=True, max_length=100)
    brand_name = models.CharField(_("brand name"), blank=True, max_length=100)

    offer_count = models.IntegerField(
        _("offer count"), blank=True, null=True, default=0
    )
    low_price = models.IntegerField(
        _("low price"), blank=True, null=True, default=0
    )
    high_price = models.IntegerField(
        _("high price"), blank=True, null=True, default=0
    )
    price_currency = models.CharField(
        _("price currency"),
        blank=True,
        max_length=100,
        default="JPY",
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
        "classifications.CategoryClassification",
        verbose_name=_("category classifications"),
        blank=True,
        related_name="CategoryProductDocument",
        limit_choices_to={"classification_type": ClassificationType.CATEGORY},
    )

    region_classifications = models.ManyToManyField(
        "classifications.RegionClassification",
        verbose_name=_("region classifications"),
        blank=True,
        related_name="RegionProductDocument",
        limit_choices_to={"classification_type": ClassificationType.REGION},
    )

    country_classifications = models.ManyToManyField(
        "classifications.CountryClassification",
        verbose_name=_("country classifications"),
        blank=True,
        related_name="CountryProductDocument",
        limit_choices_to={"classification_type": ClassificationType.COUNTRY},
    )

    city_classifications = models.ManyToManyField(
        "classifications.CityClassification",
        verbose_name=_("city classifications"),
        blank=True,
        related_name="CityProductDocument",
        limit_choices_to={"classification_type": ClassificationType.CITY},
    )

    season_classifications = models.ManyToManyField(
        "classifications.SeasonClassification",
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

    def clear_classifications(self):
        self.category_classifications.clear()
        self.region_classifications.clear()
        self.country_classifications.clear()
        self.city_classifications.clear()
        self.season_classifications.clear()

    def add_classifications(self, classification_type, slug):
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

    def classify(self):
        from ..serializers import ProductDocumentSerializer

        product = ProductDocumentSerializer(instance=self).data
        product.pop("id")
        response = self._meta.model.search(
            query={
                "percolate": {
                    "field": "query",
                    "document": product,
                },
            }
        )

        self.clear_classifications()

        for item in response["hits"]["hits"]:
            source = item["_source"]["_meta"]["classification"]
            classification_type = source["classification_type"]
            slug = source["slug"]
            self.add_classifications(
                classification_type=classification_type,
                slug=slug,
            )

    def index_product(self):
        from ..serializers import ProductDocumentSerializer

        product = ProductDocumentSerializer(instance=self).data
        doc_id = product.pop("id")
        self._meta.model.index_document(
            id=doc_id,
            document=product,
        )
