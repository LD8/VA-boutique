from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Item


class IndexView(ListView):
    '''landing page'''
    model = Category
    template_name = 'boutique/index.html'
    context_object_name = 'categories'


class ItemListView(ListView):
    '''item page'''
    # model = Category
    template_name = 'boutique/items.html'
    context_object_name = 'categories'
    paginate_by = 12

    def get_object(self):
        # obj = super().get_object()
        obj = get_object_or_404(Category, pk=self.kwargs.get('category_pk'))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'women' in self.request.GET:
            context['categories'] = Category.objects.filter(women=True)
        elif 'men' in self.request.GET:
            context['categories'] = Category.objects.filter(men=True)
        if 'category_pk' in self.request.GET:
            
        return context

class ItemDetailView(DetailView):
    '''item page'''
    # model = Item
    template_name = 'boutique/item.html'
    context_object_name = 'item'

    def get_object(self):
        return get_object_or_404(Item, pk=self.kwargs['item_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
