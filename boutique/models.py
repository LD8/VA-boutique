from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ExifTags
from django.db import models
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

    def __str__(self):
        return ("Men's " + self.name) if self.gender == 2 else ("Women's " + self.name)


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
        return ("Men's " + self.name) if self.category.gender == 2 else ("Women's " + self.name)


class Item(models.Model):
    '''Each item represents a product'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField(default='0')
    discount = models.IntegerField(null=True, blank=True)
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return self.name

    def discounted_price(self):
        '''to calculate the price after discount'''
        return int(self.price * (100 - self.discount) * 0.01)


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


@receiver(post_save, sender=ItemImage, dispatch_uid="update_image_item")
def update_image(sender, instance, **kwargs):
    '''to implement rotate function'''
    if instance.image:
        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        fullpath = BASE_DIR + instance.image.url
        rotate_image(fullpath)
