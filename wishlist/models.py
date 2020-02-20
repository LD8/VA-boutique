from django.db import models
from django.contrib.auth.models import User
from boutique.models import Item
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile


class WishList(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    slug = models.SlugField(max_length=20, default='', editable=False)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return "{}s Wish List".format(self.profile.user.username.capitalize())

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('wishlist:wish-list', kwargs={'slug': self.slug,})


@receiver(post_save, sender=Profile, dispatch_uid="create_user_wish_list")
def create_wish_list(sender, instance, created, **kwargs):
    user_wish_list, created = WishList.objects.get_or_create(profile=instance)
    user_wish_list.save()
