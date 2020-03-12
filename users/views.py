from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Profile
from django.contrib.auth import login


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    query_pk_and_slug = True


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['name', 'email', 'phone', 'address']
    template_name = 'users/profile_update.html'


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
            messages.warning(self.request, _(
                "Please complete your profile information"))
            if next:
                return redirect(next)
            return redirect('users:profile-update', new_user.profile.pk, new_user.profile.slug)

        return render(self.request, self.template_name, {'form': self.form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = {
            'content': "Реплики сумок и брендовой одежды недорого. Натуральная кожа. Купить реплики сумок Chanel. Купить реплики сумок Луи Виттон недорого Москва.",
            'title': "Стильная обувь.Реплики ремней. Качественные вещи",
        }
        return context


# def logout_view(request):
#     logout(request)
#     return redirect('/')