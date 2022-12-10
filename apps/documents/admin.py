from django.contrib import admin

from .models import (CategoryClassification, CityClassification,
                     CountryClassification, ProductDocument,
                     RegionClassification, SeasonClassification)


@admin.register(ProductDocument)
class ProductDocumentAdmin(admin.ModelAdmin):
    search_fields = ('category_classifications', )
    filter_horizontal = ('category_classifications', 'region_classifications',
                         'country_classifications', 'city_classifications',
                         'season_classifications', )


class BaseClassificationAdmin(admin.ModelAdmin):
    list_display = ('order', 'slug', 'name',)
    fields = ('slug', 'name', 'order', 'synonyms', 'antonyms')


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
