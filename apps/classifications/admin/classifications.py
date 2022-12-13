from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from ..models import (
    CategoryClassification,
    CityClassification,
    CountryClassification,
    RegionClassification,
    SeasonClassification,
)


class BaseClassificationAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "name",
    )
    actions = ["index_classifications"]
    search_fields = ("slug", "name")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "slug",
                    "name",
                    "order",
                ),
            },
        ),
        (
            _("Query options"),
            {
                "fields": (
                    "synonyms",
                    "antonyms",
                ),
            },
        ),
    )

    @admin.action(description=_("Index classification rules."))
    def index_classifications(self, request, queryset):
        for obj in queryset:
            obj.index_classification()
        self.message_user(
            request,
            _("Classification rules indexed."),
            messages.SUCCESS,
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.index_classification()


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
