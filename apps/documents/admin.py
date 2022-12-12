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
    list_display = ("title",)
    search_fields = ("category_classifications",)
    filter_horizontal = (
        "category_classifications",
        "region_classifications",
        "country_classifications",
        "city_classifications",
        "season_classifications",
    )
    actions = ["classify_documents", "clear_classifications"]

    @admin.action(description=_("Classify documents"))
    def classify_documents(self, request, queryset):
        for obj in queryset:
            obj.classify()
        self.message_user(
            request,
            _("Classified products."),
            messages.SUCCESS,
        )

    @admin.action(description=_("Clear classifications"))
    def clear_classifications(self, request, queryset):
        for obj in queryset:
            obj.clear_classifications()
        self.message_user(
            request,
            _("Cleared classifications."),
            messages.SUCCESS,
        )


class BaseClassificationAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "slug",
        "name",
    )
    fields = ("slug", "name", "order", "synonyms", "antonyms")
    actions = ["index_classifications"]

    @admin.action(description=_("Index classification rules."))
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        percolator = ClassificationPercolatorSerializer(instance=obj).data
        ProductDocument.index_document(
            id=percolator["id"],
            document=percolator,
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
class SeasonClassificationAdmin(BaseClassificationAdmin):
    pass
