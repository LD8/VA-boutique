from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from boutique.models import Item
from django.utils.text import slugify
from django.urls import reverse
from django.utils.translation import gettext, gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True,
                            verbose_name=_('Your name'))
    email = models.EmailField(max_length=100, blank=True, verbose_name=_("Your Email"))
    phone = models.IntegerField(
        blank=True, null=True, verbose_name=_('Your cell phone number'))
    address = models.CharField(max_length=100, blank=True,
                            verbose_name=_('What is your address'))

    slug = models.SlugField()

    def __str__(self):
        return self.profile_name

    @property
    def profile_name(self):
        return "{}s Profile".format(self.user.username)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.profile_name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.pk,
            'slug': self.slug,
        }
        return reverse('users:profile', kwargs=kwargs)


@receiver(post_save, sender=User, dispatch_uid="create_profile")
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile, dispatch_uid="create_wish_list")
def create_wish_list(sender, instance, created, **kwargs):
    from wishlist.models import WishList
    if created:
        user_wish_list = WishList.objects.create(profile=instance)
