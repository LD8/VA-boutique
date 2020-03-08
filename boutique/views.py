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
    context = {'categories_shown': Category.objects.get_categories_by_gender(gender).annotate(
        Count('item')).exclude(item__count=0).prefetch_related('subcategory_set__item_set')}
    return render(request, 'boutique/show_all.html', context)


def show_category(request, pk):
    context = {'categories_shown': Category.objects.filter(
        pk=pk).prefetch_related('subcategory_set', 'item_set')}
    return render(request, 'boutique/show_all.html', context)


def show_subcategory(request, pk):
    context = {'subcategories_shown': SubCategory.objects.filter(
        pk=pk).select_related('category')}

    subcategory = SubCategory.objects.get(pk=pk)

    context['filters'] = {
        'subcategory': subcategory,
        'brand_pk': None,
        'min_price': None,
        'max_price': None,
    }

    context['brands'] = get_brands(subcategory.item_set.all())

    print(context)
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
    print(request.GET)
    print(kwargs)
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
        subcategory = get_object_or_404(SubCategory, pk=sub_pk)
        items = subcategory.item_set.all()
        context['filters']['subcategory'] = subcategory
    else:
        items = Item.objects.all()

    # It's important to insert 'brands' in context now to get all brands
    context['brands'] = get_brands(items)

    if brand_pk:
        items = items.filter(brand__pk=brand_pk).select_related('brand')

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

    context['items'] = items.prefetch_related('itemimage_set')
    print(context)
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
        raise Http404


# class SubCategoryListView(ListView):
#     model = SubCategory
#     template_name = 'boutique/show_subcategory.html'


class CategoryListView(ListView):
    '''display a list of items'''
    model = Category
    # paginate_by = 1
    template_name = 'boutique/show_category.html'
    context_object_name = 'category_shown'

    def get_queryset(self):
        qs = super().get_queryset().get_categories_with_item()
        self.gender = self.kwargs.get('gender')  # reuse in context
        gender = self.gender
        request = self.request

        # fetch filter-form data
        self.category_selected = request.GET.get('category_selected')
        self.brand_selected = request.GET.get('brand_selected')
        self.min_price = request.GET.get('min_price')
        self.max_price = request.GET.get('max_price')

        if gender == 'women':
            self.gender_number = 1
        elif gender == 'men':
            self.gender_number = 2
        else:
            raise Http404

        get_category_selected = Category.objects.filter(
            gender=self.gender_number, name__iexact=self.category_selected).first()
        category_selected_pk = get_category_selected.pk if get_category_selected else None

        get_subcategory_selected = SubCategory.objects.filter(
            category__gender=self.gender_number, name__iexact=self.category_selected).first()
        subcategory_selected_pk = get_subcategory_selected.pk if get_subcategory_selected else None

        category_pk = category_selected_pk if category_selected_pk else self.kwargs.get(
            'category_pk')
        subcategory_pk = subcategory_selected_pk if subcategory_selected_pk else self.kwargs.get(
            'subcategory_pk')

        # print('\nself.kwargs:\n', gender, category_pk, subcategory_pk)

        if gender and not category_pk and not subcategory_pk:
            qs = qs.get_categories_by_gender(gender)
            # print('\nCategoryLV_qs_gender= ', '\n', qs, '\n', gender, '\n')
            return qs

        elif gender and category_pk:
            qs = qs.filter(pk=category_pk)
            # print('\nCategoryLV_qs_category= ', '\n', qs, '\n')
            return qs

        elif gender and subcategory_pk:
            qs = SubCategory.objects.annotate(Count('item')).exclude(
                item__count=0).filter(pk=subcategory_pk)
            self.context_object_name = 'subcategory_shown'
            # print('\nCategoryLV_qs_sub_category= ', '\n', qs, '\n')
            return qs

    def get_validated_cats(self):
        categories_validated = []
        subcategories_validated = []
        items_validated = []

        brand_selected = self.brand_selected
        min_price = self.min_price
        if min_price == '' or min_price is None:
            min_price = 0
        max_price = self.max_price
        if max_price == '' or max_price is None:
            max_price = 999999

        for item in Item.objects.select_related('category', 'subcategory', 'tag').filter(category__gender=self.gender_number):
            if int(min_price) <= item.final_price < int(max_price):
                if brand_selected is None or brand_selected == 'бренд' or item.brand.name == brand_selected:
                    items_validated.append(item)
                    if item.category not in categories_validated:
                        categories_validated.append(item.category)
                    if item.subcategory not in subcategories_validated:
                        subcategories_validated.append(item.subcategory)

        return categories_validated, subcategories_validated, items_validated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()

        cat_valid, subcat_valid, items_valid = self.get_validated_cats()
        context['filter_context'] = {
            'gender': self.gender,
            'gender_number': self.gender_number,
            'category_selected': self.category_selected,
            'brand_selected': self.brand_selected,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'categories_validated': cat_valid,
            'subcategories_validated': subcat_valid,
            'items_validated': items_valid,
        }

        # print(context)
        return context
