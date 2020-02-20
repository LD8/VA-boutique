from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render, redirect
from boutique.models import Item
from django.urls import reverse
from users.models import Profile
from .models import WishList
from django.contrib import messages


# @method_decorator(login_required, name='dispatch')
# class WishListDetailView(DetailView):
#     model = WishList
#     template_name = 'wishlist/wish_list.html'
#     query_pk_and_slug = True


@login_required
def wish_list(request, **kwargs):
    profile = get_object_or_404(Profile, user=request.user)
    wish_list = get_object_or_404(WishList, profile=profile)
    return render(request, 'wishlist/wish_list.html', {'wishlist': wish_list,})


@login_required
def add_wish(request, **kwargs):
    item_to_add = get_object_or_404(Item, pk=kwargs.get('item_pk'))
    wish_list = get_object_or_404(WishList, profile=request.user.profile)
    if item_to_add in wish_list.items.all():
        messages.info(request, "It's already in your wish-list!")
        return redirect('boutique:item', kwargs.get('item_pk'))
    else:
        wish_list.items.add(item_to_add)
        wish_list.save()
        messages.info(request, "Item added to wish-list!")
        return redirect('wishlist:wish-list', wish_list.pk, wish_list.slug)


@login_required
def del_wish(request, **kwargs):
    wish_list = get_object_or_404(WishList, profile=request.user.profile)
    item_to_del = wish_list.items.get(pk=kwargs.get('item_pk'))
    if item_to_del:
        wish_list.items.remove(item_to_del)
        messages.info(request, "Item removed from your wish list!")

    return redirect('wishlist:wish-list', wish_list.pk, wish_list.slug)
