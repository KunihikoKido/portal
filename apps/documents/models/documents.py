from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .classifications import ClassificationType


class BaseDocument(models.Model):
    url = models.URLField(_('url'), unique=True)
    title = models.CharField(_('title'), blank=True, max_length=100)
    description = models.TextField(_('description'), blank=True)
    image_url = models.URLField(_('image url'), blank=True)

    pub_date = models.DateTimeField(
        verbose_name=_("publication date"),
        default=timezone.now,
        db_index=True,
        help_text=_('Set the date and time you want your '
                    'post to be published.')
    )

    is_active = models.BooleanField(
        _('active'), default=False,
        help_text=_(
            'Designates whether this article should be treated as active. '
            'Unselect this instead of deleting articles.'
        ),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title or self.url


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

    rating = models.PositiveIntegerField(
        _('review rating'), default=0, blank=False, null=False)
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
