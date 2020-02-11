from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ExifTags
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import os


class Category(models.Model):
    '''Category for men's and women's items'''
    gender = models.IntegerField(choices=[
        (1, 'Women'),
        (2, 'Men'),
    ], default=1)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta():
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name.capitalize() + ' for ' + self.get_gender_display()

    def get_category_url(self):
        return reverse('boutique:category', kwargs={'gender': self.get_gender_display(), 'category_pk': self.pk})


class SubCategory(models.Model):
    '''Sub-category for the categories (not mandatory)'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta():
        verbose_name = 'Sub-category'
        verbose_name_plural = 'Sub-categories'

    def __str__(self):
        return self.category.get_gender_display() + ' ' + self.name

    def get_subcategory_url(self):
        return reverse('boutique:subcategory', kwargs={'gender': self.category.get_gender_display(), 'category_pk': self.category.pk, 'subcategory_pk': self.pk})


class Tag(models.Model):
    '''Items have tag will have according discount percentage'''
    tag_discount_percentage = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(100)])
    slogan = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.slogan if self.slogan else self.slogan_default

    @property
    def slogan_default(self):
        return 'Purchase NOW for extra {}% off!'.format(self.tag_discount_percentage)


class Item(models.Model):
    '''Each item represents a product'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    discount_percentage = models.IntegerField(verbose_name='Discount Percentage', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT, null=True, blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return self.name

    @property
    def discounted_price(self): # changed from get_discounted_price
        '''to calculate the price after discount'''
        return int(self.price * (100 - self.discount_percentage) * 0.01)

    @property
    def final_price(self): # changed from get_final_price
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
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='index_carousel_images')
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta():
        verbose_name = 'Index Carousel'
        verbose_name_plural = 'Index Carousels'
        ordering = ['-uploaded_date']


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='itemimages', null=True, blank=True)


def rotate_image(filepath):
    '''rotate images based on their original orientation, 
    this solves the problem that uploaded images are in wrong orientation'''
    try:
        image = Image.open(filepath)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(filepath)
        image.close()
    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        pass

# doc: pre_save and post_save: https://docs.djangoproject.com/en/3.0/ref/signals/#pre-save 
@receiver(post_save, sender=ItemImage, dispatch_uid="update_image_item")
def update_image(sender, instance, **kwargs):
    '''to implement rotate function'''
    if instance.image:
        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        fullpath = BASE_DIR + instance.image.url
        rotate_image(fullpath)
