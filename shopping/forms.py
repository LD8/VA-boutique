from django import forms
from .models import AnonymousOrder
from users.models import Profile
from django.utils.translation import gettext_lazy as _


class AnonymousOrderForm(forms.ModelForm):
    class Meta:
        model = AnonymousOrder
        fields = ['customer_name', 'customer_location',
                  'customer_phone', 'customer_email']
        labels = {
            'customer_name': _("Your full name"),
            'customer_location': _("Where do you currently live?"),
            'customer_phone': _("Your phone number"),
            'customer_email': _("Your email"),
        }


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].required = True
        # self.fields['email'].required = True
        # self.fields['phone'].required = True
        # self.fields['address'].required = True
        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone', 'address']
