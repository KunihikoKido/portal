from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from ..models import ProductDocument
from ..serializers import ProductDocumentSerializer


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
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
        "index_productdocuments",
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
                ),
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
        (
            _("Review options"),
            {
                "fields": (
                    "rating",
                    "review_count",
                )
            },
        ),
        (
            _("Offer options"),
            {"fields": ("offer_count",)},
        ),
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
    def index_productdocuments(self, request, queryset):
        for obj in queryset:
            document = ProductDocumentSerializer(instance=obj).data
            ProductDocument.index_document(
                id=document["id"],
                document=document,
            )

        self.message_user(
            request,
            _("Product documents indexed."),
            messages.SUCCESS,
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        document = ProductDocumentSerializer(instance=obj).data
        ProductDocument.index_document(
            id=document["id"],
            document=document,
        )
