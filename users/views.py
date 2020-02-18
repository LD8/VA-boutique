from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile


@method_decorator(login_required, name='dispatch')
class RegisterView(TemplateView):
    '''Render registration page'''
    template_name = 'registration/register.html'
    form = UserCreationForm()

    def get(self, *args, **kwargs):
        context = {'form': self.form}
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        self.form = UserCreationForm(data=self.request.POST)
        if self.form.is_valid():
            new_user = self.form.save()
            login(request, new_user)
            return redirect('boutique:index')

        return render(self.request, self.template_name, {'form': self.form})


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    query_pk_and_slug = True
    

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['name', 'email', 'phone', 'city']
    template_name = 'users/profile_update.html'
    