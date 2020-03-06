from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q
from django.db.models import Prefetch
from django.urls import reverse
from django.db import models
import os


class CategoryQuerySet(models.QuerySet):
    def get_categories_with_item(self):
        return self.annotate(Count('item')).exclude(item__count=0).prefetch_related('subcategory_set')

    def get_categories_by_gender(self, gender):
        if gender == 'women':
            return self.filter(gender=1)
        if gender == 'men':
            return self.filter(gender=2)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_categories_with_item(self):
        return self.get_queryset().get_categories_with_item()

    def get_categories_by_gender(self, gender):
        return self.get_queryset().get_category_by_gender(gender)


class Category(models.Model):
    '''Category for men's and women's items'''
    gender = models.IntegerField(choices=[
        (1, 'women'),
        (2, 'men'),
    ], default=1)
    name = models.CharField(max_length=100, verbose_name=_('Category Name'))
    description = models.CharField(max_length=300, blank=True, verbose_name=_('Category Description'))
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    objects = CategoryManager()

    class Meta():
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['gender', 'name']

    def __str__(self):
        return self.name.capitalize() + ' for ' + self.get_gender_display().capitalize()

    def get_category_url(self):
        return reverse('boutique:show-category', kwargs={'gender': self.get_gender_display(), 'category_pk': self.pk})

    def load_related_item(self):
        return self.item_set.select_related('brand', 'tag')

    def load_related_subcategory(self):
        return self.subcategory_set.all()


class SubCategory(models.Model):
    '''Sub-category for the categories (not mandatory)'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=_('Sub-category Name'))
    description = models.CharField(max_length=300, blank=True, verbose_name=_('Sub-category Description'))
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta():
        verbose_name = _('Sub-category')
        verbose_name_plural = _('Sub-categories')
        ordering = ['name']

    def __str__(self):
        return self.category.get_gender_display() + ' ' + self.name

    def get_subcategory_url(self):
        return reverse('boutique:show-subcategory', kwargs={'gender': self.category.get_gender_display(), 'subcategory_pk': self.pk})

    def load_related_item(self):
        return self.item_set.select_related('brand', 'tag')


class Tag(models.Model):
    '''Items have tag will have according discount percentage'''
    tag_discount_percentage = models.IntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name=_('Tag (discount percentage)'))
    slogan = models.CharField(max_length=200, blank=True, verbose_name=_('Slogan for tags'))

    def __str__(self):
        return self.slogan if self.slogan else self.slogan_default

    @property
    def slogan_default(self):
        return 'Purchase NOW for extra {}% off!'.format(self.tag_discount_percentage)


class Brand(models.Model):
    '''the brands of the items'''
    name = models.CharField(max_length=50, verbose_name=_('Brand Name'))
    description = models.TextField(blank=True, verbose_name=_('Brand Description'))

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def item_numbers_under_this_brand(self):
        return self.item_set.count()


class ItemQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = Item.objects.all()
        query = query

        def is_valid_queryparam(param):
            '''check if the query parameter(the search input) is valid'''
            return param is not '' and param is not None

        # if type to search initially
        if is_valid_queryparam(query):
            qs = qs.filter(
                Q(category__name__icontains=query) |
                Q(category__description__icontains=query) |
                Q(subcategory__name__icontains=query) |
                Q(subcategory__description__icontains=query) |
                Q(name__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        # print('\nfinal qs is as following: ', qs, '\n')
        return qs


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Item(models.Model):
    '''Each item represents a product'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ForeignKey(
        Tag, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, default=3)

    name = models.CharField(max_length=100, unique=True, verbose_name=_('Item Name'))
    description = models.TextField(blank=True, verbose_name=_('Item Description'))
    price = models.IntegerField(default=0)
    discount_percentage = models.IntegerField(verbose_name=_('Discount Percentage'), default=0, validators=[
                                              MinValueValidator(0), MaxValueValidator(100)])
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    objects = ItemManager()

    class Meta:
        ordering = ['-uploaded_date', '-discount_percentage']

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):  # changed from get_discounted_price
        '''to calculate the price after discount'''
        return int(self.price * (100 - self.discount_percentage) * 0.01)

    @property
    def final_price(self):  # changed from get_final_price
        '''to calculate the tagged price 5% off'''
        return int(self.price * (100 - self.discount_percentage - self.tag.tag_discount_percentage) * 0.01
                   ) if self.tag else int(self.discounted_price)

    @property
    def total_discount_percentage(self):
        '''to calculate the total discount'''
        return (self.discount_percentage + self.tag.tag_discount_percentage
                ) if self.tag is not None else self.discount_percentage

    def get_item_url(self):
        return reverse('boutique:item', kwargs={'pk': self.pk})


class IndexCarousel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Carousel Title'))
    description = models.TextField(verbose_name=_('Carousel Text'))
    image = models.ImageField(
        upload_to='index_carousel_images', verbose_name=_('Image (Size: 2100 x 1400 px)'))
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = _('Index Carousel')
        verbose_name_plural = _('Index Carousels')
        ordering = ['uploaded_date']


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='itemimages', null=True, blank=True)
