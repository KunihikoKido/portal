from django import forms
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from ..models import Recommendation


class RecommendationAdminForm(forms.ModelForm):
    execute_indexing_process = forms.BooleanField(
        label=_("Execute indexing process"),
        required=False,
        initial=True,
        help_text=_(
            "If you wish to run the process, "
            "check the box and save the data."
        ),
    )

    class Meta:
        model = Recommendation
        fields = "__all__"


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    form = RecommendationAdminForm
    list_display = (
        "title",
        "start_datetime",
        "end_datetime",
        "is_active",
    )
    list_filter = ("is_active",)
    date_hierarchy = "start_datetime"
    actions = ["index_recommendation_rules"]
    search_fields = ("title",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "link",
                    "prefix_url",
                ),
            },
        ),
        (
            _("publication"),
            {
                "fields": (
                    "start_datetime",
                    "end_datetime",
                    "is_active",
                ),
            },
        ),
        (
            _("Actions"),
            {
                "fields": ("execute_indexing_process",),
            },
        ),
    )

    @admin.action(description=_("Index recommendation rules."))
    def index_recommendation_rules(self, request, queryset):
        for obj in queryset:
            obj.index_recommendation()
        self.message_user(
            request,
            _("Recommendation rules indexed."),
            messages.SUCCESS,
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if form.cleaned_data["execute_indexing_process"]:
            obj.index_recommendation()
            self.message_user(
                request,
                _("Recommendation rules indexed."),
                messages.SUCCESS,
            )

    def delete_model(self, request, obj):
        obj.delete_recommendation()
        return super().delete_model(request, obj)
