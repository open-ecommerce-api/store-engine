from django.contrib import admin
from apps.products.models import Product, ProductOption, ProductOptionItem, ProductVariant
from apps.attributes.models import Attribute, AttributeItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductOptionItemInline(admin.TabularInline):
    model = ProductOptionItem
    extra = 0


@admin.register(ProductOption)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ProductOptionItemInline]


@admin.register(ProductOptionItem)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('item',)

# @admin.register(ProductVariant)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name',)
