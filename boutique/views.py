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
        context['index_h1_title_text'] = 'Качественные копии/реплики брендов в интернет магазине VA boutique. Cтильная одежда и аксессуары премиум качества по доступным ценам! Бесплатная доставка по России!'
        return context


class NewListView(ListView):
    model = Item
    template_name = 'boutique/new.html'
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.all()[:40]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = {
            'content': "Купить копии брендовой одежды, обуви, сумок высочайшего качества, а также по доступным ценам с доставкой по всему миру!",
            'keywords': "реплика одежды, брендовая одежда копии брендов, люкс копии брендовой одежды и аксессуаров",
            'title': "Купить копии / реплики брендовой одежды с бесплатной доставкой по всей России",
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
            'content': "Купить копии брендовой одежды, обуви, сумок высочайшего качества, а также по доступным ценам с доставкой по всему миру!",
            'keywords': "реплика одежда, копии брендов интернет магазин",
            'title': "Купить копии / реплики брендовой одежды и аксессуаров со скидкой",
        }
        return context


def show_all(request, gender):
    """ Display categories and subcategories by gender """
    context = {
        'categories_shown': Category.objects.get_categories_by_gender(gender).get_categories_with_item().prefetch_related('subcategory_set__item_set'),
        'brands': Brand.objects.annotate(
            brand_pk=F('pk'),
            brand_name=F('name')).values(
            'brand_pk', 'brand_name').order_by('brand_name'),
    }

    if gender == 'men':
        for_men_or_women = 'для мужчин'
        # h1 title shown on 'show all men items' page
        context['h1_title_text'] = 'Стильные мужские сумки и аксессуары премиум качества в VA boutique!'
    elif gender == 'women':
        for_men_or_women = 'для женщин'
        # h1 title shown on 'show all women items' page
        context['h1_title_text'] = 'Реплики модных сумок, аксессуаров и обуви премиум качества по доступным ценам! Бесплатная доставка по России!'
    else:
        raise Http404

    context['meta'] = {
        'content': "Купить реплики / копии брендов, сумок и аксессуаров премиум качества по доступным ценам с бесплатной доставкой.",
        'keywords': "Копии мужской и женской брендовой одежды",
        'title': "Копии мужской и женской брендовой одежды в интернет магазине VA boutique",
    }

    return render(request, 'boutique/show_all.html', context)


def show_category(request, pk):
    """ Display a category and its subcategories """
    cat_queryset = Category.objects.filter(pk=pk).prefetch_related(
        'subcategory_set__item_set')
    cat = cat_queryset.first()

    context = {
        'cat': cat,
        'filters': {'category': cat, },
        'brands': get_brands(cat.item_set),
        'meta': {
            'content': cat.meta_content,
            'keywords': cat.meta_keywords,
            'title': cat.meta_title,
        },
    }

    if cat.subcategory_set.count() == 0:
        return render(request, 'boutique/show_barren_category.html', context)
    else:
        return render(request, 'boutique/show_fertile_category.html', context)


def show_subcategory(request, pk):
    """ Display a subcategory """
    subcategory = get_object_or_404(SubCategory, pk=pk)
    context = {
        'subcategories_shown': SubCategory.objects.filter(pk=pk).select_related('category'),
        'filters': {'subcategory': subcategory, },
        'brands': get_brands(subcategory.item_set.all()),
        'meta': {
            'content': subcategory.meta_content,
            'keywords': subcategory.meta_keywords,
            'title': subcategory.meta_title,
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

    # meta title generator
    # filter_content = ""
    # meta_title = f"Ваш результат поиска {filter_content}"

    # initialise queryset: items
    if sub_pk:
        subcategory = get_object_or_404(SubCategory, pk=sub_pk)
        context['filters']['subcategory'] = subcategory
        items = subcategory.item_set.select_related('brand')
        # filter_content = f": {subcategory.name}"
    elif cat_pk:
        category = get_object_or_404(Category, pk=cat_pk)
        context['filters']['category'] = category
        items = category.item_set.select_related('brand')
        # filter_content = f": {category.name}"
    else:
        items = Item.objects.select_related('brand')
        # filter_content = f": все категории"

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
    context['meta'] = {
        'content': "Купить реплики / копии брендов, сумок и аксессуаров премиум качества по доступным ценам с бесплатной доставкой.",
        'keywords': "Реплики  брендов, Копии брендов, Купить реплику сумки, Купить копию сумки, Интернет-магазин реплик сумок, Сумки реплики брендов, Копии сумок известных брендов, Сумки копии брендов интернет магазин",
        'title': "Копии известных брендов / Купить реплики брендов в Москве - Интернет-магазин VA boutique",
    }
    return render(request, 'boutique/filtered_items.html', context)


class ItemDetailView(DetailView):
    '''display an individual item'''
    model = Item
    template_name = 'boutique/item.html'
    queryset = Item.objects.prefetch_related('itemimage_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_name = context['item'].name
        item_cat_pk = context['item'].category.pk
        # if the item belongs to cosmetic category:
        if item_cat_pk == 6:
            context['is_cosmetics'] = True
            context['meta'] = {
                'content': "Интернет магазин Китайской и Корейской костетики",
                'keywords': "китайская косметика, корейская косметика, недорого, бесплатная доставка",
                'title': f"купить {item_name}",
            }
        else:
            context['meta'] = {
                'content': f"Интернет-магазин  VA boutique представляет копию {item_name}. Данная модель произведена из материалов высокого качества. Купить этот и другие товары Вы можете в Москве или оформив доставку в любой другой город России.",
                'keywords': f"Копия {item_name}, Купить копию item name, Реплика item name в Москве",
                'title': f"Купить копию {item_name} в Москве - Интернет-магазин  VA boutique",
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
            'content': "Купить реплики / копии брендов, сумок и аксессуаров премиум качества по доступным ценам с бесплатной доставкой.",
            'keywords': "Реплики  брендов, Копии брендов, Купить реплику сумки, Купить копию сумки, Интернет-магазин реплик сумок, Сумки реплики брендов, Копии сумок известных брендов, Сумки копии брендов интернет магазин",
            'title': "Копии известных брендов / Купить реплики брендов в Москве - Интернет-магазин VA boutique",
        }
        return context
