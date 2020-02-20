from django.contrib.auth.models import User
from boutique.models import Item
from users.models import Profile
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class OrderItem(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.item.name


class Order(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET(get_sentinel_user))
    items = models.ManyToManyField(OrderItem)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)
    ref_number = models.CharField(max_length=15, blank=True)
    active = models.BooleanField(default=False, verbose_name='Order Active')

    def __str__(self):
        return "{}_{}".format(self.profile.user.username, self.ref_number)

    def get_order_items(self):
        return self.items.all()

    def get_order_total(self):
        return sum([item.item.final_price() for item in self.get_order_items])

    class Meta():
        ordering = ['-active', '-date_ordered']

class AnonymousOrder(models.Model):
    ref_number = models.CharField(max_length=15, blank=True, unique=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=50, verbose_name='My name')
    customer_location = models.CharField(max_length=50, verbose_name='My Location')
    customer_phone = models.IntegerField(verbose_name='My phone number')
    customer_email = models.EmailField(max_length=100, verbose_name='My email')
    date_ordered = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, verbose_name='Order Active')

    def __str__(self):
        return "Anonymous Order No.:{}; Item: {}".format(self.ref_number, self.item)

    def get_absolute_url(self):
        return reverse('shopping:buy-now-order', self.item.pk, self.ref_number)
    
    class Meta():
        verbose_name = 'Anonymous Order'
        ordering = ['-active', '-date_ordered']
