from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify

class VipOrder(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Your name'))
    email = models.EmailField(max_length=100, blank=True, verbose_name=_('Your email'))
    phone = models.IntegerField(verbose_name=_('Your cell phone number'))
    address = models.CharField(max_length=30, verbose_name=_('What is your address?'))
    item_description = models.TextField(verbose_name=_("Describe the item briefly"))
    item_image1 = models.ImageField(upload_to='vip_order', verbose_name=_("Upload a photo of the item"))
    item_image2 = models.ImageField(upload_to='vip_order', blank=True, null=True, verbose_name=_("Upload another photo of the item (optional)"))
    item_image3 = models.ImageField(upload_to='vip_order', blank=True, null=True, verbose_name=_("Upload another photo of the item (optional)"))
    slug = models.SlugField(max_length=20, default='', editable=False)

    def __str__(self):
        return self.order_name

    @property
    def order_name(self):
        return "{}s order".format(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.order_name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('vip:vip-order', kwargs={'slug': self.slug,})