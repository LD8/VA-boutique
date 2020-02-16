from django.db import models
from django.contrib.auth.models import User
from boutique.models import Item
from django.urls import reverse
from django.utils.text import slugify

class ShoppingBag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    added_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def __str__(self):
        return "{}'s Shopping Bag".format(user.name.capitalize())

    class Meta():
        ordering = ['-added_date']
