from django.contrib import admin
from .models import Category, SubCategory, Item, ItemImage


class ItemImageInline(admin.TabularInline):
    model = ItemImage


class SubCategoryInline(admin.TabularInline):
    model = SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubCategoryInline,
    ]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        ItemImageInline,
    ]

class ItemInline(admin.TabularInline):
    model = Item

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]
    exclude = ['item.category']