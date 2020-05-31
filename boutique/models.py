from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q, F
from django.db.models import Prefetch
from django.urls import reverse
from django.db import models
import os
from django.db.models import prefetch_related_objects


class CategoryQuerySet(models.QuerySet):
    def get_categories_with_item(self):
        return self.annotate(Count('item')).exclude(item__count=0)

    def get_categories_by_gender(self, gender):
        if gender == 'women':
            return self.filter(gender=1)
        elif gender == 'men':
            return self.filter(gender=2)
        else:
            return self.all()

    def get_category_brands(self, pk):
        # brands_pk: a flat list of brand pks in a category
        brands_set = self.filter(pk=pk)[0].item_set.order_by().annotate(
            brand_pk=F('brand__pk'),
            brand_name=F('brand__name')).values(
            'brand_pk', 'brand_name').distinct().order_by('brand_name')
        # a list of brand names
        return brands

    def load_related_subcategory(self):
        return self.subcategory_set.all()

    def load_related_item(self):
        return self.item_set.all()


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_categories_with_item(self):
        return self.get_queryset().get_categories_with_item()

    def get_categories_by_gender(self, gender):
        return self.get_queryset().get_categories_by_gender(gender)

    def get_category_brands(self, pk):
        return self.get_queryset().get_category_brands(pk)

    def load_related_subcategory(self):
        return self.get_queryset().load_related_subcategory()

    def load_related_item(self):
        return self.get_queryset().load_related_item()


class Category(models.Model):
    '''Category for men's and women's items'''
    gender = models.IntegerField(choices=[
        (1, 'women'),
        (2, 'men'),
    ], default=1)
    name = models.CharField(max_length=100, verbose_name=_('Category Name'))
    description = models.CharField(
        max_length=300, blank=True, verbose_name=_('Category Description'))
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    meta_content = models.CharField(
        max_length=155, verbose_name='Meta Content (Max: 155 characters)', blank=True)
    meta_keywords = models.CharField(
        max_length=155, verbose_name='Meta keywords (Max: 155 characters)', blank=True)
    meta_title = models.CharField(
        max_length=55, verbose_name='Meta Title (Max: 55 characters)', blank=True)

    objects = CategoryManager()

    class Meta():
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['gender', 'name']

    def __str__(self):
        return '{} for {}'.format(self.name, self.get_gender_display())

    def get_category_url(self):
        return reverse('boutique:show-category', kwargs={'pk': self.pk})
        # return reverse('boutique:show-category', kwargs={'gender': self.get_gender_display(), 'category_pk': self.pk})


class SubCategoryQuerySet(models.QuerySet):
    def get_subcategories_with_item(self):
        return self.annotate(Count('item')).exclude(item__count=0).prefetch_related('item_set', 'category')

    def load_related_item(self):
        items = self.item_set.all()
        prefetch_related_objects(items, 'itemimage_set')
        return items


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return SubCategoryQuerySet(self.model, using=self._db)

    def get_subcategories_with_item(self):
        return self.get_queryset().get_subcategories_with_item()

    def load_related_item(self):
        return self.get_queryset().load_related_item()


class SubCategory(models.Model):
    '''Sub-category for the categories (not mandatory)'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100, verbose_name=_('Sub-category Name'))
    description = models.CharField(
        max_length=300, blank=True, verbose_name=_('Sub-category Description'))
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    meta_content = models.CharField(
        max_length=155, verbose_name='Meta Content (Max: 155 characters)', blank=True)
    meta_keywords = models.CharField(
        max_length=155, verbose_name='Meta keywords (Max: 155 characters)', blank=True)
    meta_title = models.CharField(
        max_length=55, verbose_name='Meta Title (Max: 55 characters)', blank=True)

    objects = SubCategoryManager()

    class Meta():
        verbose_name = _('Sub-category')
        verbose_name_plural = _('Sub-categories')
        ordering = ['name']

    def __str__(self):
        return self.category.get_gender_display() + ' ' + self.name

    def get_subcategory_url(self):
        return reverse('boutique:show-subcategory', kwargs={'pk': self.pk})


class Tag(models.Model):
    '''Items have tag will have according discount percentage'''
    tag_discount_percentage = models.IntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name=_('Tag (discount percentage)'))
    slogan = models.CharField(
        max_length=200, blank=True, verbose_name=_('Slogan for tags'))

    def __str__(self):
        return self.slogan if self.slogan else self.slogan_default

    @property
    def slogan_default(self):
        return 'Purchase NOW for extra {}% off!'.format(self.tag_discount_percentage)


class Brand(models.Model):
    '''the brands of the items'''
    name = models.CharField(max_length=50, verbose_name=_('Brand Name'))
    description = models.TextField(
        blank=True, verbose_name=_('Brand Description'))

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
        if query is not '' and query is not None:
            qs = qs.filter(
                Q(category__name__icontains=query) |
                Q(category__description__icontains=query) |
                Q(subcategory__name__icontains=query) |
                Q(subcategory__description__icontains=query) |
                Q(name__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        return qs


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Item(models.Model):
    '''Each item represents a product'''
    # ----- ForeignKeys ----- #
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.ForeignKey(
        Tag, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, default=7)

    # ----- status ----- #
    in_stock = models.BooleanField(default=True, verbose_name=_(
        'In Stock (untick when out of stock)'))

    # ----- Attributes ----- #
    name = models.CharField(max_length=100, unique=True,
                            verbose_name=_('Item Name'))
    description = models.TextField(
        blank=True, verbose_name=_('Item Description'))
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    # ----- price section ----- #
    price = models.IntegerField(default=0, verbose_name=_('Original Price'))
    discount_percentage = models.IntegerField(
        verbose_name=_('Discount Percentage'), default=0, validators=[
            MinValueValidator(0), MaxValueValidator(100)])
    discounted_price = models.IntegerField(
        verbose_name=_('Discounted Price (Calculated automatically)'), blank=True, null=True)
    total_discount_percentage = models.IntegerField(
        verbose_name=_('Total Discount Percentage (Calculated automatically)'), blank=True, null=True)
    final_price = models.IntegerField(
        verbose_name=_('Final Price (Calculated automatically)'), blank=True, null=True)

    # ----- object manager ----- #
    objects = ItemManager()

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.discounted_price = int(
            self.price * (100 - self.discount_percentage) * 0.01)
        self.total_discount_percentage = int(self.discount_percentage + self.tag.tag_discount_percentage
                                             ) if self.tag else self.discount_percentage
        self.final_price = int(self.price * (100 - self.discount_percentage - self.tag.tag_discount_percentage) * 0.01
                               ) if self.tag else self.discounted_price
        super().save(*args, **kwargs)

    def get_item_url(self):
        return reverse('boutique:item', kwargs={'pk': self.pk})


class IndexCarousel(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Carousel Title'))
    description = models.TextField(verbose_name=_('Carousel Text'))
    text_colour = models.CharField(
        max_length=100,
        choices=[
            ('white', _('White')),
            ('khaki', _('Khaki')),
            ('lightseagreen', _('Light Sea Green')),
            ('orange', _('Orange')),
            ('maroon', _('Maroon')),
            ('lightgrey', _('Lightgrey')),
            ('rgba(30, 30, 30, 0.9)', _('bizdiz Darkgrey')),
            ('darkgrey', _('Darkgrey')),
            ('black', _('Black')),
        ], default='white')
    image = models.ImageField(
        upload_to='index_carousel_images', verbose_name=_('Image (Size: 1200 x 800 px)'))
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
