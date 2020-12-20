from django.contrib import admin

from .models import ProductRating
from .models import AverageAge
from .models import AverageRating
# Register your models here.

@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    readonly_fields = ['clothing_id']

@admin.register(AverageAge)
class AverageAgeAdmin(admin.ModelAdmin):
    readonly_fields = ['avg_id']

@admin.register(AverageRating)
class AverageRatingAdmin(admin.ModelAdmin):
    readonly_fields = ['avg_id']