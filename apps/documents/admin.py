from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from .models import (
    CategoryClassification,
    CityClassification,
    CountryClassification,
    ProductDocument,
    RegionClassification,
    SeasonClassification,
)
from .serializers import ClassificationPercolatorSerializer


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    search_fields = ("category_classifications",)
    filter_horizontal = (
        "category_classifications",
        "region_classifications",
        "country_classifications",
        "city_classifications",
        "season_classifications",
    )


class BaseClassificationAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "slug",
        "name",
    )
    fields = ("slug", "name", "order", "synonyms", "antonyms")
    actions = ["index_classifications"]

    @admin.action(description="Index classification rules")
    def index_classifications(self, request, queryset):
        for obj in queryset:
            percolator = ClassificationPercolatorSerializer(instance=obj).data
            ProductDocument.index_document(
                id=percolator["id"],
                document=percolator,
            )
        self.message_user(
            request,
            _("Classification rules indexed."),
            messages.SUCCESS,
        )


@admin.register(CategoryClassification)
class CategoryClassificationAdmin(BaseClassificationAdmin):
    pass


@admin.register(RegionClassification)
class RegionClassificationAdmin(BaseClassificationAdmin):
    pass


@admin.register(CountryClassification)
class CountryClassificationAdmin(BaseClassificationAdmin):
    pass


@admin.register(CityClassification)
class CityClassificationAdmin(BaseClassificationAdmin):
    pass


@admin.register(SeasonClassification)
class SeasonClassificationAdmin(admin.ModelAdmin):
    pass
