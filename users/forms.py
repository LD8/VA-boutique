from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django import forms
# from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_('The username does not exist'))
            if not user.check_password(password):
                raise forms.ValidationError(_('Incorrect password'))
            if not user.is_active:
                # Translators: After a long period of time without logging in, the user can become an inactive user, the admin can reactivate the user, this message is to tell the user this information
                raise forms.ValidationError(
                    _('The user is not active, please contact admin...'))
        return super().clean(*args, **kwargs)

# class UserRegisterForm(forms.ModelForm):
#     password1 = forms.CharField(
#         label=_("Пароль"),
#         strip=False,
#         widget=forms.PasswordInput
#         )
#     password2 = forms.CharField(
#         label=_("Подтверждение пароля"),
#         strip=False,
#         widget=forms.PasswordInput,
#         help_text=_("Введите пароль ещё раз")
#         )

#     class Meta:
#         model = User
#         fields = ['username', 'password1', 'password2', ]

#     def clean(self, *args, **kwargs):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError('Пароли не совпадают')
#         return super().clean(*args, **kwargs)
