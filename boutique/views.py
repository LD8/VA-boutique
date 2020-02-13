from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Item, SubCategory, IndexCarousel, Brand
from django.db.models import Q


class IndexView(ListView):
    '''landing page'''
    model = Category
    template_name = 'boutique/index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carousels'] = IndexCarousel.objects.all()
        return context


class CategoryListView(ListView):
    '''display a list of items'''
    model = Category
    # paginate_by = 1

    def get_queryset(self):
        qs = super().get_queryset()
        gender = self.kwargs.get('gender')
        category_pk = self.kwargs.get('category_pk')
        subcategory_pk = self.kwargs.get('subcategory_pk')

        print('self.kwargs:\n', gender, category_pk, subcategory_pk)

        if gender:
            if gender == 'Women':
                qs = qs.filter(gender=1)
            elif gender == 'Men':
                qs = qs.filter(gender=2)
            print('\nCategoryLV_qs_gender= ', '\n', qs, '\n', gender, '\n')
            self.context_object_name = 'categories_shown'
            return qs

        elif category_pk:
            qs = qs.filter(pk=category_pk)
            print('\nCategoryLV_qs_category= ', '\n', qs, '\n')
            self.context_object_name = 'category_shown'
            return qs

        elif subcategory_pk:
            qs = get_object_or_404(SubCategory, pk=subcategory_pk)
            print('\nCategoryLV_qs_sub_category= ', '\n', qs, '\n')
            self.context_object_name = 'subcategory_shown'
            print(self.context_object_name)
            return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = Brand.objects.all()


        print(context)
        return context


class FilterCategoryListView(CategoryListView):
    """ search within that category/subcategory/all categories under one gender """

    def __init__(self):
        self.category_selected = self.request.GET.get('category_selected')
        self.brand_selected = self.request.GET.get('brand_selected')
        self.min_price = self.request.GET.get('min_price')
        self.max_price = self.request.GET.get('max_price')
        print(self.category_selected, '\n', self.min_price, '\n', self.max_price, '\n', self.brand, '\n',
              )

    def get_queryset(self):
        if is_valid_queryparam(self.category_selected) and 'Категори' not in self.category_selected:
            qs = Category.filter()
            pass
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['min_price'] = self.min_price
        context['max_price'] = self.max_price
        context['brand_selected'] = self.brand if self.brand != 'бренд' else None

        print('\nSearch_CategoryLV_qs= ', '\n', qs, '\n')
        return context


class ItemDetailView(DetailView):
    '''display an individual item'''
    model = Item
    template_name = 'boutique/item.html'
    # no need to specify as default context_object_name depends on the model
    # they are actually the same (with lower case first letter)
    # context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add categories for navbar link texts
        context['categories'] = Category.objects.all()
        # print('\ncontext= ', context, '\n')
        return context


def is_valid_queryparam(param):
    '''check if the query parameter(the search input) is valid'''
    return param is not '' and param is not None


class SearchView(ListView):
    '''display search result from the search query input'''
    template_name = 'boutique/search.html'

    def get_queryset(self):
        qs = Item.objects.all()
        self.brands = Brand.objects.all()
        self.query = self.request.GET.get('query')
        self.min_price = self.request.GET.get('min_price')
        self.max_price = self.request.GET.get('max_price')
        self.brand_selected = self.request.GET.get('brand_selected')
        self.category_selected = self.request.GET.get('category_selected')

        # if type to search initially
        if is_valid_queryparam(self.query):
            qs = qs.filter(
                Q(category__name__icontains=self.query) |
                Q(category__description__icontains=self.query) |
                Q(subcategory__name__icontains=self.query) |
                Q(subcategory__description__icontains=self.query) |
                Q(name__icontains=self.query) |
                Q(brand__name__icontains=self.query) |
                Q(description__icontains=self.query)
            ).distinct()

        if is_valid_queryparam(self.category_selected) and self.category_selected != 'Категория':
            qs = qs.filter(category__name__icontains=self.category_selected)

        print('\nqs before brand filter: ', qs, '\n')

        if is_valid_queryparam(self.brand_selected) and self.brand_selected != 'бренд':
            qs = qs.filter(brand__name__icontains=self.brand_selected)

        print('\nqs after brand filter: ', qs, '\n')

        if is_valid_queryparam(self.min_price):
            # if self.request.user is not None:
            qs = qs.filter(price__gte=self.min_price)
            # else:
            #     qs = qs.filter(discounted_price__gte=min_price)

        if is_valid_queryparam(self.max_price):
            qs = qs.filter(price__lt=self.max_price)

        print('\nfinal qs is as following: ', qs, '\n')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['brands'] = self.brands
        context['query'] = self.query
        context['min_price'] = self.min_price
        context['max_price'] = self.max_price
        context['brand_selected'] = self.brand_selected if self.brand_selected != 'бренд' else None
        context['category_selected'] = self.category_selected if self.category_selected != 'категорию' else None

        print(context)
        return context
