from django.shortcuts import render, get_object_or_404
from .models import Category, Item
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import Category

# def index(request):
#     '''landing page'''
#     categories = Category.objects.all()
#     context = {'categories':categories}
#     return render(request, 'boutique/index.html', context)


class IndexView(TemplateView):
    '''landing page'''
    template_name = 'boutique/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ItemListView(ListView):
    '''item page'''
    model = Category
    # template_name = 'boutique/items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context