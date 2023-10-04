from django.contrib import admin
from apps.attributes.models import Attribute, AttributeItem


class AttributeItemInline(admin.TabularInline):
    model = AttributeItem
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [AttributeItemInline]


@admin.register(AttributeItem)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('item',)
