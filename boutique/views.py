from django.shortcuts import render, get_object_or_404, Http404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Category, Item, SubCategory, IndexCarousel, Brand
from django.db.models import F, Q, Count


class IndexView(TemplateView):
    '''landing page'''
    template_name = 'boutique/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carousels'] = IndexCarousel.objects.all()
        return context


class SalesListView(ListView):
    model = Item
    template_name = 'boutique/sales.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.select_related('tag').filter(
            Q(discount_percentage__gt=0) |
            Q(tag__tag_discount_percentage__gt=0)
        ).order_by('-discount_percentage', '-tag__tag_discount_percentage')


def show_all(request, gender):
    context = {
        'categories_shown': Category.objects.get_categories_by_gender(gender).annotate(
            Count('item')).exclude(item__count=0).prefetch_related('subcategory_set__item_set'),
        'brands': Brand.objects.annotate(
            brand_pk=F('pk'),
            brand_name=F('name')).values(
            'brand_pk', 'brand_name').order_by('brand_name')
    }
    return render(request, 'boutique/show_all.html', context)


def show_category(request, pk):
    context = {'categories_shown': Category.objects.filter(
        pk=pk).prefetch_related('subcategory_set', 'item_set')}
    return render(request, 'boutique/show_all.html', context)


def show_subcategory(request, pk):
    subcategory = SubCategory.objects.get(pk=pk)

    context = {
        'subcategories_shown': SubCategory.objects.filter(pk=pk).select_related('category'),
        'filters': {
            'subcategory': subcategory,
            'brand_pk': None,
            'min_price': None,
            'max_price': None,
        },
        'brands': get_brands(subcategory.item_set.all())
    }
    return render(request, 'boutique/show_subcategory.html', context)


def get_brands(item_queryset):
    """ Get all brands of items """
    brands_dict = item_queryset.order_by().annotate(
        brand_pk=F('brand__pk'),
        brand_name=F('brand__name')).values(
            'brand_pk', 'brand_name').distinct().order_by('brand_name')
    # Output: <ItemQuerySet [{'brand_pk': 4, 'brand_name': 'Dior'}, {...}, ...]>
    return brands_dict


def filter_item(request, pk=None, **kwargs):
    """ Page shows filtered items """
    sub_pk = pk
    brand_pk = request.GET.get('brand_pk')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    context = {}
    context['filters'] = {
        'subcategory': None,
        'brand_pk': brand_pk,
        'min_price': min_price,
        'max_price': max_price,
    }

    # initialise queryset: items
    if sub_pk:
        # subcategory = get_object_or_404(SubCategory, pk=sub_pk)
        subcategory = SubCategory.objects.get(pk=sub_pk)
        context['filters']['subcategory'] = subcategory
        items = subcategory.item_set.all()
    else:
        items = Item.objects.all()

    # It's important to insert 'brands' in context now to get all brands
    context['brands'] = get_brands(items)

    if brand_pk:
        items = items.filter(brand__pk=brand_pk)

    if min_price:
        if request.user.is_authenticated:
            items = items.filter(final_price__gte=min_price)
        else:
            items = items.filter(discounted_price__gte=min_price)

    if max_price:
        if request.user.is_authenticated:
            items = items.filter(final_price__lte=max_price)
        else:
            items = items.filter(discounted_price__lte=max_price)

    context['items'] = items
    return render(request, 'boutique/filtered_items.html', context)


class ItemDetailView(DetailView):
    '''display an individual item'''
    model = Item
    template_name = 'boutique/item.html'
    queryset = Item.objects.prefetch_related('itemimage_set')


class SearchView(ListView):
    '''display search result from the search query input'''
    template_name = 'boutique/search.html'

    def get_queryset(self):
        request = self.request
        self.query = request.GET.get('query', None)

        if self.query is not None:
            qs = Item.objects.search(self.query)
            return qs
        return Item.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context
