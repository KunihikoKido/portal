from django import forms
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from ..models import ProductDocument


class ProductDocumentAdminForm(forms.ModelForm):

    execute_indexing_process = forms.BooleanField(
        label=_("Execute indexing process"),
        required=False,
        help_text=_(
            "If you wish to run the process, "
            "check the box and save the data."
        ),
    )
    execute_classify_process = forms.BooleanField(
        label=_("Execute classify process"),
        required=False,
        help_text=_(
            "If you wish to run the process, "
            "check the box and save the data."
        ),
    )

    class Meta:
        model = ProductDocument
        fields = "__all__"


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    form = ProductDocumentAdminForm
    list_display = ("title",)
    search_fields = ("title", "product_id")
    autocomplete_fields = (
        "category_classifications",
        "region_classifications",
        "country_classifications",
        "city_classifications",
        "season_classifications",
    )
    actions = [
        "index_products",
        "classify_documents",
        "clear_classifications",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "url",
                    "title",
                    "description",
                    "image_url",
                    "pub_date",
                    "is_active",
                )
            },
        ),
        (
            _("Product options"),
            {
                "fields": (
                    "product_id",
                    "brand_name",
                    "low_price",
                    "high_price",
                    "price_currency",
                )
            },
        ),
        (_("Review options"), {"fields": ("rating", "review_count")}),
        (_("Offer options"), {"fields": ("offer_count",)}),
        (
            _("Classification options"),
            {
                "fields": (
                    "category_classifications",
                    "region_classifications",
                    "country_classifications",
                    "city_classifications",
                    "season_classifications",
                )
            },
        ),
        (
            _("Actions"),
            {
                "fields": (
                    "execute_classify_process",
                    "execute_indexing_process",
                )
            },
        ),
    )

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

    @admin.action(description=_("Index product documents."))
    def index_products(self, request, queryset):
        for obj in queryset:
            obj.index_product()

        self.message_user(
            request,
            _("Product documents indexed."),
            messages.SUCCESS,
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if form.cleaned_data["execute_indexing_process"]:
            obj.index_product()
        if form.cleaned_data["execute_classify_process"]:
            obj.classify()

    def delete_model(self, request, obj):
        obj.delete_product()
        return super().delete_model(request, obj)
