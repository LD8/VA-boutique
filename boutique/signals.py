from django.db.models.signals import post_save, post_delete
from boutique.models import ItemImage, IndexCarousel
from django.dispatch import receiver
from PIL import Image, ExifTags
import os


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


@receiver(post_delete, sender=ItemImage, dispatch_uid="delete_image_item")
def delete_image(sender, instance, **kwargs):
    '''to delete related image after the item is deleted'''
    if instance.image:
        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        fullpath = BASE_DIR + instance.image.url
        os.remove(fullpath)


post_delete.connect(delete_image, sender=IndexCarousel,
                    dispatch_uid="delete_image_carousel")
