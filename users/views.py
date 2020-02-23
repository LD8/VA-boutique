from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile
# from .forms import UserLoginForm, UserRegisterForm
# from django.contrib.auth import (
#     authenticate,
#     login,
#     logout,
# )


# def login_view(request):
#     next = request.GET.get('next')
#     form = UserLoginForm(request.POST or None)

#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         if next:
#             return redirect(next)
#         return redirect('/')

#     return render(request, 'registration/login.html', {'form': form})


# def register_view(request):
#     next = request.GET.get('next')
#     form = UserRegisterForm(request.POST or None)

#     if form.is_valid():
#         new_user = form.save(commit=False)
#         password = form.cleaned_data.get('password2')
#         new_user.set_password(password)
#         new_user.save()
#         user = authenticate(username=new_user.username, password=password)
#         login(request, user)
#         if next:
#             return redirect(next)
#         return redirect('/')

#     return render(request, 'registration/register.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    query_pk_and_slug = True


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['name', 'email', 'phone', 'city']
    template_name = 'users/profile_update.html'

# def logout_view(request):
#     logout(request)
#     return redirect('/')


class RegisterView(TemplateView):
    '''Render registration page'''
    template_name = 'registration/register.html'
    form = UserCreationForm()

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'form': self.form})

    def post(self, *args, **kwargs):
        next = self.request.GET.get('next')
        self.form = UserCreationForm(data=self.request.POST)
        if self.form.is_valid():
            new_user = self.form.save()
            login(self.request, new_user)
            if next:
                return redirect(next)
            return redirect('users:profile-update', new_user.profile.pk, new_user.profile.slug)

        return render(self.request, self.template_name, {'form': self.form})
