# from django.db import models
# from django.contrib.auth.models import User
# from boutique.models import Item
# from django.urls import reverse
# from django.utils.text import slugify


# class BagItem(models.Model):
#     item = models.OneToOneField(Item, on_delete=models.CASCADE)


# class ShoppingBag(models.Model):
#     owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     items = models.ManyToManyField(BagItem)
#     added_date = models.DateTimeField(auto_now=True)
#     slug = models.SlugField()

#     def __str__(self):
#         return "{}'s Shopping Bag".format(user.name.capitalize())

#     class Meta():
#         ordering = ['-added_date']
