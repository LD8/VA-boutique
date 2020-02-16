from django.shortcuts import render
from django.views.generic import ListView
from .models import ShoppingBag
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class ShoppingBagView(ListView):
    model = ShoppingBag
    template_name = 'users/shopping_bag.html'

    @method_decorator(login_required)
    def add_to_shopping_bag(self, item_pk):
        pass

    @method_decorator(login_required)
    def delete_from_shopping_bag(self, item_pk):
        pass

    @method_decorator(login_required)
    def order_now(self):
        pass
