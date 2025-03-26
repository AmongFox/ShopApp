from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ProductModel


class ProductAdmin(admin.ModelAdmin):
    model = ProductModel
    list_display = (
        'name',
        'description',
        'price',
        'discount',
        'quantity',
        'created_date',
        'created_by',
        'archived',
        'preview',  # ResizedImageField field
    )
    list_filter = ('created_date', 'created_by', 'archived')
    search_fields = ('name', 'description', 'created_by__username')
    ordering = ('name', 'price', 'discount', 'quantity', 'created_date')

    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Цена и наличие', {'fields': ('price', 'discount', 'quantity')}),
        ('Статус и изображение', {'fields': ('archived', 'preview')}),  # ResizedImageField field
        ('Владелец', {'fields': ('created_by',)}),
    )


admin.site.register(ProductModel, ProductAdmin)
