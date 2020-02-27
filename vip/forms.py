from django import forms
from .models import VipOrder


class VipOrderForm(forms.ModelForm):
    class Meta:
        model = VipOrder
        fields = ['name', 'email', 'phone', 'address', 'item_description',
                  'item_image1', 'item_image2', 'item_image3']
