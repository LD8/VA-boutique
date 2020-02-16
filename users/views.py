from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from boutique.models import Category


class RegisterView(TemplateView):
    '''Render registration page'''
    template_name = 'registration/register.html'
    form = UserCreationForm()

    def get(self, *args, **kwargs):
        context = {'form': self.form}
        context['categories'] = Category.objects.get_categories_with_item()
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        self.form = UserCreationForm(data=self.request.POST)
        if self.form.is_valid():
            new_user = self.form.save()
            login(request, new_user)
            return redirect('boutique:index')

        return render(self.request, self.template_name, {'form': self.form})


def profile(request):
    '''render user's profile page'''
    posts = request.user.post_set.all()
    comments = request.user.comment_set.all()
    comments_on_posts_not_authored_by_me = []
    for comment in comments:
        if comment.post not in posts:
            comments_on_posts_not_authored_by_me.append(comment)
    return render(request, 'users/profile.html', {
        'posts': posts,
        'comments': comments,
        'other_comments': comments_on_posts_not_authored_by_me})
