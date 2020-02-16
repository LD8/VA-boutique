from django.contrib import admin
from .models import (
    Category, 
    SubCategory, 
    Item,
    ItemImage, 
    Tag, 
    IndexCarousel, 
    Brand,
    )

admin.site.site_header = 'VA-Boutique | Site Administration | Such Fun!!!'
admin.site.index_title = 'Manage Administrators and upload/Update Items'
admin.site.site_title = 'VA-Boutique'
admin.site.register(Tag)
admin.site.register(IndexCarousel)
admin.site.register(Brand)


class ItemImageInline(admin.TabularInline):
    model = ItemImage


class SubCategoryInline(admin.TabularInline):
    model = SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        SubCategoryInline,
    ]
    list_display = ('name','gender','description','uploaded_date')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        ItemImageInline,
    ]
    list_display = ('name','brand','price','discounted_price','final_price','discount_percentage','tag','category','subcategory')
    search_fields = ['name']



# a bug of SubCategoryAdmin: force to complete all 3 of the item info before submission
# class ItemInline(admin.TabularInline):
#     model = Item

# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     inlines = [
#         ItemInline,
#     ]
#     exclude = ['item.category']
