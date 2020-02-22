from django.db import models


class VipOrder(models.Model):
    name = models.CharField(max_length=100, verbose_name='Your name')
    email = models.EmailField(max_length=100, blank=True)
    phone = models.IntegerField(verbose_name='Your cell phone number')
    city = models.CharField(max_length=30, verbose_name='Which city are you in?')
    item_description = models.TextField()
    item = models.ImageField(upload_to='vip_order/')
    item = models.ImageField(upload_to='vip_order/', null=True)
    item = models.ImageField(upload_to='vip_order/', null=True)

    def __str__(self):
        return self.name

    @property
    def order_name(self):
        return "{}s order".format(self.name)
