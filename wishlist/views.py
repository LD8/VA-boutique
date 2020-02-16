from django.shortcuts import render
from django.views.generic import ListView
from .models import WishList
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class WishListView(ListView):
    model = WishList
    template_name = 'users/wish_list.html'

    def get_queryset(self):
        qs = super().get_queryset().get(user=self.user)
        return qs

    def add_to_wish_list(self, item_pk):
        if not self.item_set.get(pk=item_pk):
            item_to_add = get_object_or_404(Item, pk=item_pk)
            self.items.add(item_to_add)
            self.save()
        else:
            redirect

    def delete_from_wish_list(self, item_pk):
        item_to_delete = get_object_or_404(Item, pk=item_pk)

