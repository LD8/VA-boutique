from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile
from .models import Order


# to create a shopping_bag/order whenever a profile is created
@receiver(post_save, sender=Profile, dispatch_uid="create_profile_order")
def create_profile_order(sender, instance, created, **kwargs):
    if not Order.objects.get(profile=instance, is_ordered=False):
        profile_order, created = Order.objects.get_or_create(
            profile=instance, 
            ref_number="{}'s shopping bag".format(instance.user.username),
            )
        profile_order.save()
