from django.db import models
from django.contrib.auth.models import User
from boutique.models import Item
from django.urls import reverse
from django.utils.text import slugify


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    added_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=20, default='', editable=False)

    class Meta():
        ordering = ['-added_date']

    def __str__(self):
        return self.name

    @property
    def name(self):
        return "{}'s Wish List".format(self.user.username.capitalize())

    def get_absolute_url(self):
        return reverse('users:wish-list', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True).lower()
        super().save()
