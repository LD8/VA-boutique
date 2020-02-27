from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
# below imports: signal
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class VipOrder(models.Model):
    ref_number = models.CharField(max_length=15, blank=True, unique=True, verbose_name=_("VIP Order Number"))
    active = models.BooleanField(default=False, verbose_name=_("VIP Order Active?"))
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, verbose_name=_('Your name'))
    email = models.EmailField(max_length=100, verbose_name=_('Your email'))
    phone = models.IntegerField(verbose_name=_('Your cell phone number'))
    address = models.CharField(max_length=30, verbose_name=_('What is your address?'))
    item_description = models.TextField(verbose_name=_("Describe the item briefly"))
    item_image1 = models.ImageField(upload_to='vip_order', verbose_name=_("Upload a photo of the item"))
    item_image2 = models.ImageField(upload_to='vip_order', blank=True, null=True, verbose_name=_("Upload another photo of the item (optional)"))
    item_image3 = models.ImageField(upload_to='vip_order', blank=True, null=True, verbose_name=_("Upload another photo of the item (optional)"))

    class Meta():
        verbose_name = _('VIP Order')
        verbose_name_plural = _('VIP Orders')
        ordering = [ '-active', '-date_created']

    def __str__(self):
        return "Номер заказа: {}".format(self.ref_number)

    # def get_absolute_url(self):
    #     return reverse('vip:vip-order', kwargs={'slug': self.slug,})



@receiver(post_delete, sender=VipOrder, dispatch_uid="delete_vip_order_image")
def delete_vip_order_image(sender, instance, **kwargs):
    '''to delete related image after the order is deleted'''
    def del_vip_image(instance_dot_image):
        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        fullpath = BASE_DIR + instance_dot_image.url
        os.remove(fullpath)

    del_vip_image(instance.item_image1)
    if instance.item_image2:
        del_vip_image(instance.item_image2)
    if instance.item_image3:
        del_vip_image(instance.item_image3)


        

