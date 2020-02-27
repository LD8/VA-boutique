from django.db.models.signals import post_save
from django.dispatch import receiver
from wishlist.models import WishList
from .models import Order


@receiver(post_save, sender=WishList, dispatch_uid="create_shopping_bag")
def create_shopping_bag(sender, instance, created, **kwargs):
    if created:
        shopping_bag = Order.objects.create(
            profile=instance.profile,
            ref_number="{}'s shopping bag".format(
                instance.profile.user.username.capitalize()),
        )


