# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import ShoppingBag


# to create a shopping_bag whenever a user is created
# @receiver(post_save, sender=User, dispatch_uid="create_user_shopping_bag")
# def create_shopping_bag(sender, instance, created, **kwargs):
#     user_shopping_bag, created = ShoppingBag.objects.get_or_create(
#         user=instance)
