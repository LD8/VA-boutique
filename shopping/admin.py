from django.contrib import admin
from .models import AnonymousOrder, Order


@admin.register(AnonymousOrder)
class AnonymousOrderAdmin(admin.ModelAdmin):
    list_display = ('ref_number', 'active', 'item', 'customer_name', 'customer_location',
                    'customer_phone', 'customer_email', 'date_ordered')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ref_number', 'active', 'is_ordered',
                    'profile', 'date_ordered')
