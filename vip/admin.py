from django.contrib import admin
from .models import VipOrder


@admin.register(VipOrder)
class VipOrderAdmin(admin.ModelAdmin):
    list_display = (
        'ref_number',
        'name',
        'active',
        'email',
        'phone',
        'address',
        'item_description',
        'item_image1',
        'item_image2',
        'item_image3',
    )

