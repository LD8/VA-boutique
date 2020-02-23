from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from boutique.models import Item
from django.utils.text import slugify
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True,
                            verbose_name='Your name')
    email = models.EmailField(max_length=100, blank=True)
    phone = models.IntegerField(
        blank=True, null=True, verbose_name='Your cell phone number')
    city = models.CharField(max_length=30, blank=True,
                            verbose_name='Which city are you in?')
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



# @receiver(post_save, sender=User, dispatch_uid="create_user_profile")
# def create_profile(sender, instance, created, **kwargs):
#     user_profile, created = Profile.objects.get_or_create(user=instance)
#     if created:
#         user_profile.save()

#     from wishlist.models import WishList
#     from shopping.models import Order
#     user_wish_list, created = WishList.objects.get_or_create(profile=user_profile)
#     if created:
#         user_wish_list.save()

#     if not Order.objects.get(profile=user_profile, is_ordered=False):
#         new_shopping_list = Order.objects.create(
#             profile=user_profile, 
#             ref_number="{}'s shopping bag".format(user_profile.user.username),
#             )

@receiver(post_save, sender=User, dispatch_uid="create_profile")
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile, dispatch_uid="create_wish_list")
def create_wish_list(sender, instance, created, **kwargs):
    from wishlist.models import WishList
    if created:
        user_wish_list = WishList.objects.create(profile=instance)

