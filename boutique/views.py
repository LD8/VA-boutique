from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Item, SubCategory


class IndexView(ListView):
    '''landing page'''
    model = Category
    template_name = 'boutique/index.html'
    context_object_name = 'categories'


class CategoryListView(ListView):
    '''display a list of items'''
    model = Category
    template_name = 'boutique/items.html'
    context_object_name = 'categories'
    # paginate_by = 12

    def get_queryset(self):
        # get original queryset: Category.objects.all()
        qs = super().get_queryset()

        # filter men/women
        if self.kwargs.get('gender') == 'Women':
            qs = qs.filter(gender=1) 
        elif self.kwargs['gender'] == 'Men':
            qs = qs.filter(gender=2)

        if self.kwargs.get('category_pk'):
            qs = qs.filter(pk=self.kwargs.get('category_pk'))

        print('\nqs= ', qs, '\n')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add categories for navbar link texts
        context['categories'] = Category.objects.all()

        if self.kwargs.get('subcategory_pk'):
            context['subcategory_shown'] = get_object_or_404(
                SubCategory, pk=self.kwargs.get('subcategory_pk'))
            context['item_list'] = Item.objects.filter(subcategory=self.kwargs.get('subcategory_pk'))
            print('\ncontext with subcat= ', context, '\n')
            return context

        context['category_shown'] = self.get_queryset()

        if self.kwargs.get('category_pk'):
            context['item_list'] = Item.objects.filter(category=self.kwargs.get('category_pk'))

        # print('\ncontext= ', context, '\n')
        return context


class ItemDetailView(DetailView):
    '''display an individual item'''
    model = Item
    template_name = 'boutique/item.html'
    # context_object_name = 'item'

    def get_object(self):
        # why this doesn't work with `obj = super().get_object()` executed here????
        obj = get_object_or_404(Item, pk=self.kwargs.get('item_pk'))

        # print('\nget_queryset()= ', type(obj), obj.name, '\n')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add categories for navbar link texts
        context['categories'] = Category.objects.all()

        # print('\ncontext= ', context, '\n')
        return context
