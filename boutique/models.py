from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ExifTags
from django.db import models
import os


class Category(models.Model):
    '''Category for men's and women's items'''
    men = models.BooleanField()
    women = models.BooleanField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    class Meta():
        verbose_name_plural = 'Categories'

    def __str__(self):
        return ("Men's " + self.name) if self.men else ("Women's " + self.name)


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
        return ("Men's " + self.name) if self.category.men else ("Women's " + self.name)


class Item(models.Model):
    '''Item model with maximum 5 images uploaded'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField(default='0')
    discount = models.IntegerField(null=True, blank=True)
    uploaded_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    image_1 = models.ImageField(upload_to='items/')
    image_2 = models.ImageField(upload_to='items/', blank=True)
    image_3 = models.ImageField(upload_to='items/', blank=True)
    image_4 = models.ImageField(upload_to='items/', blank=True)
    image_5 = models.ImageField(upload_to='items/', blank=True)

    class Meta:
        ordering = ['-uploaded_date']

    def __str__(self):
        return self.name

    def discounted_price(self):
        '''to calculate the price after discount'''
        return int(self.price * (100 - self.discount) * 0.01)


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


@receiver(post_save, sender=Item, dispatch_uid="update_image_item")
def update_image(sender, instance, **kwargs):
    '''iterate through the images uploaded to implement rotate function'''
    dic = {
        'image_1': instance.image_1,
        'image_2': instance.image_2,
        'image_3': instance.image_3,
        'image_4': instance.image_4,
        'image_5': instance.image_5,
    }
    # probably there's a better way to iterate through the images in the model
    # what if there's more images to be iterate through?
    for k, instanceImage in dic.items():
        if instanceImage:
            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))
            fullpath = BASE_DIR + instanceImage.url
            rotate_image(fullpath)
