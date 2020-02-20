from django import forms
from .models import AnonymousOrder
from users.models import Profile

class AnonymousOrderForm(forms.ModelForm):
    class Meta:
        model = AnonymousOrder
        fields = ['customer_name', 'customer_location', 'customer_phone', 'customer_email']
        labels = {
            'customer_name': 'Your Name', 
            'customer_location': "Where do you currently live?",
            'customer_phone': "Your phone number",
            'customer_email': "Your email",
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone', 'city']