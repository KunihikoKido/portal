from django.contrib import admin

from .models import Classification, ProductDocument


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'classification_type')
    list_filter = ('classification_type',)


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    pass
