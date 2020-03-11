from django.shortcuts import render, get_object_or_404, Http404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Category, Item, SubCategory, IndexCarousel, Brand
from django.db.models import F, Q, Count
from datetime import datetime, timedelta


class IndexView(TemplateView):
    '''landing page'''
    template_name = 'boutique/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carousels'] = IndexCarousel.objects.all()
        return context


class NewListView(ListView):
    model = Item
    template_name = 'boutique/new.html'
    context_object_name = 'items'

    def get_queryset(self):
        qs = Item.objects.filter(uploaded_date__lte=datetime.now()-timedelta(days=30)).order_by('-uploaded_date')[:31]
        if qs.count() < 30:
            qs = Item.objects.all()[:31]
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = {
            'content': "Онлайн бутик VA это стильная одежда и аксессуары премиум качество по доступным ценам! Бесплатная доставка по России!",
            'title': "",
        }
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = {
            'content': "Онлайн бутик VA это стильная одежда и аксессуары премиум качество по доступным ценам! Бесплатная доставка по России!",
            'title': "",
        }
        return context


def show_all(request, gender):
    context = {
        'categories_shown': Category.objects.get_categories_by_gender(gender).get_categories_with_item().prefetch_related('subcategory_set__item_set'),
        'brands': Brand.objects.annotate(
            brand_pk=F('pk'),
            brand_name=F('name')).values(
            'brand_pk', 'brand_name').order_by('brand_name'),
        'meta': {
            'content': "Купить реплики модных сумок, аксессуаров и обуви. Качественные женские сумки и обувь известных брендов Интернет магазин брендовых сумок и аксессуаров.",
            'title': "VA Реплики Сумки | Бижутерия | Обувь | Ремни | Очки",
        },
    }
    return render(request, 'boutique/show_all.html', context)


def show_category(request, pk):
    cat_queryset = Category.objects.filter(pk=pk)
    cat = cat_queryset.first()
    context = {
        'categories_shown': cat_queryset.prefetch_related('subcategory_set__item_set'),
        'filters': {'category': cat, },
        'brands': get_brands(cat.item_set),
        'show_all_cat_items_flag': True if cat.subcategory_set.count() == 0 else False,
        'meta': {
            'content': "Онлайн бутик VA это стильная одежда и аксессуары премиум качество по доступным ценам! Бесплатная доставка по России!",
            'title': "",
        },
    }
    return render(request, 'boutique/show_all.html', context)


def show_subcategory(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    context = {
        'subcategories_shown': SubCategory.objects.filter(pk=pk).select_related('category'),
        'filters': {'subcategory': subcategory, },
        'brands': get_brands(subcategory.item_set.all()),
        'meta': {
            'content': "Онлайн бутик VA это стильная одежда и аксессуары премиум качество по доступным ценам! Бесплатная доставка по России!",
            'title': "",
        },
    }
    return render(request, 'boutique/show_subcategory.html', context)


def get_brands(item_queryset):
    """ Get all brands of items """
    brands_dict_lst = item_queryset.order_by().annotate(
        brand_pk=F('brand__pk'),
        brand_name=F('brand__name')).values(
            'brand_pk', 'brand_name').distinct().order_by('brand_name')
    # Output: <ItemQuerySet [{'brand_pk': 4, 'brand_name': 'Dior'}, {...}, ...]>
    return brands_dict_lst


def filter_item(request, sub_pk=None, cat_pk=None, **kwargs):
    """ Page shows filtered items """
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
        subcategory = get_object_or_404(SubCategory, pk=sub_pk)
        context['filters']['subcategory'] = subcategory
        items = subcategory.item_set.select_related('brand')
    elif cat_pk:
        category = get_object_or_404(Category, pk=cat_pk)
        context['filters']['category'] = category
        items = category.item_set.select_related('brand')
    else:
        items = Item.objects.select_related('brand')

    # It's important to insert 'brands' in context now to get all brands
    context['brands'] = get_brands(items)

    if brand_pk:
        items = items.filter(brand__pk=brand_pk)
        if not sub_pk:
            # if user filtered from show-all page, no subcat selected
            context['brand_selected_from_all'] = Brand.objects.get(
                pk=brand_pk).name

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = {
            'content': "Онлайн бутик VA это стильная одежда и аксессуары премиум качество по доступным ценам! Бесплатная доставка по России!",
            'title': "",
        }
        return context


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
        context['meta'] = {
            'content': "Онлайн бутик VA это стильная одежда и аксессуары премиум качество по доступным ценам! Бесплатная доставка по России!",
            'title': "",
        }
        return context
