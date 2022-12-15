from django import forms
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from ..models import (
    CategoryClassification,
    CityClassification,
    Classification,
    CountryClassification,
    RegionClassification,
    SeasonClassification,
)


class ClassificationAdminForm(forms.ModelForm):
    execute_classify_process = forms.BooleanField(
        label=_("Execute classify process"),
        required=False,
        initial=True,
        help_text=_(
            "If you wish to run the process, "
            "check the box and save the data."
        ),
    )

    class Meta:
        model = Classification
        fields = "__all__"


class BaseClassificationAdmin(admin.ModelAdmin):
    form = ClassificationAdminForm
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
        (
            _("Actions"),
            {
                "fields": ("execute_classify_process",),
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
        if form.cleaned_data["execute_classify_process"]:
            obj.index_classification()

    def delete_model(self, request, obj):
        obj.delete_classification()
        return super().delete_model(request, obj)


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
