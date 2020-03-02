from django.contrib.auth.models import User
from boutique.models import Item
from users.models import Profile
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class OrderItem(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item.name


class Order(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    # Translators: to describes whether the customer has placed the order or not?
    is_ordered = models.BooleanField(default=False, verbose_name=_("Ordered?"))
    # Translators: The date the order was placed
    date_ordered = models.DateTimeField(auto_now=True, verbose_name=_("Order Date"))
    ref_number = models.CharField(max_length=30, blank=True, verbose_name=_("Reference Number"))
    # Translators: to describe whether the items have been delivered and the money has been received
    active = models.BooleanField(default=False, verbose_name=_("Order Active?"))

    def __str__(self):
        return "{}_{}".format(self.profile.user.username, self.ref_number)

    def get_order_items(self):
        return self.items.all()

    @property
    def order_total(self):
        return sum([item.item.final_price for item in self.get_order_items()])

    class Meta():
        verbose_name = _('Registered Order')
        verbose_name_plural = _('Registered Orders')
        ordering = ['-is_ordered', '-active', '-date_ordered']


class AnonymousOrder(models.Model):
    ref_number = models.CharField(max_length=50, blank=True, unique=True, verbose_name=_("Reference Number"))
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # Translators: For unregistered users name
    customer_name = models.CharField(max_length=50, verbose_name=_('My name'))
    # Translators: For unregistered users location
    customer_location = models.CharField(
        max_length=50, verbose_name=_('My Location'))
    # Translators: For unregistered users phone number
    customer_phone = models.CharField(max_length=50, verbose_name=_('My phone number'))
    # Translators: For unregistered users email
    customer_email = models.EmailField(max_length=100, verbose_name=_('My email'))
    # Translators: For unregistered users ordered date
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name=_("Order Date"))
    # Translators: For unregistered users  or not
    active = models.BooleanField(default=True, verbose_name=_('Order Active?'))

    def __str__(self):
        return "Anonymous Order No.:{}; Item: {}".format(self.ref_number, self.item)

    def get_absolute_url(self):
        return reverse('shopping:buy-now-order', self.item.pk, self.ref_number)

    class Meta():
        verbose_name = _('Anonymous Order')
        verbose_name_plural = _('Anonymous Orders')
        ordering = ['-active', '-date_ordered']
