from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.utils.translation import gettext, gettext_lazy as _


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Такого пользователя не существует')
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
            if not user.is_active:
                raise forms.ValidationError('Пользователь не активен')
        
        return super().clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput
        )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Введите пароль ещё раз")
        )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', ]

    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return super().clean(*args, **kwargs)
