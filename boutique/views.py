from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Item, SubCategory


class IndexView(ListView):
    '''landing page'''
    model = Category
    template_name = 'boutique/index.html'
    context_object_name = 'categories'


class ItemListView(ListView):
    '''display a list of items'''
    model = Item
    template_name = 'boutique/items.html'
    # paginate_by = 12

    def get_queryset(self):
        # get original queryset: Item.objects.all()
        qs = super().get_queryset()

        # filter items: men/women
        if self.kwargs['gender'] == 'women':
            qs = qs.filter(category__gender=1)
        elif self.kwargs['gender'] == 'men':
            qs = qs.filter(category__gender=2)

        if self.kwargs.get('category_pk'):
            qs = qs.filter(category=self.kwargs.get('category_pk'))
            if self.kwargs.get('subcategory_pk'):
                qs = qs.filter(subcategory=self.kwargs.get('subcategory_pk'))

        # print(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add categories for navbar link texts
        context['categories'] = Category.objects.all()

        if self.kwargs.get('gender') == 'women':
            context['category_shown'] = Category.objects.filter(gender=1)
        if self.kwargs.get('gender') == 'men':
            context['category_shown'] = Category.objects.filter(gender=2)

        if self.kwargs.get('category_pk'):
            context['category_shown']=get_object_or_404(Category, pk=self.kwargs.get('category_pk'))
            if self.kwargs.get('subcategory_pk'):
                context['subcategory_shown']=get_object_or_404(SubCategory, pk=self.kwargs.get('subcategory_pk'))

        print(context)
        return context


class ItemDetailView(DetailView):
    '''display an individual item'''
    model = Item
    template_name = 'boutique/item.html'
    # context_object_name = 'item'

    # def get_object(self):
    #     obj = super().get_object()
    #     obj = get_object_or_404(Item, pk=self.kwargs.get('item_pk'))
    #     print(obj)
    #     return obj

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # add categories for navbar link texts
    #     # context['categories'] = Category.objects.all()
    #     print('123')
    #     print(context)
    #     return context
