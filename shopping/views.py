from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from .models import Order, OrderItem, AnonymousOrder
from users.models import Profile
from django.contrib import messages
from .extras import ref_number_generator, anonymous_ref_number_generator
from .forms import AnonymousOrderForm, ProfileForm
from boutique.models import Item


def get_shopping_bag(request):
    profile = get_object_or_404(Profile, user=request.user)
    # get pending order as shopping_bag object
    shopping_bag, created = Order.objects.get_or_create(
        is_ordered=False, profile=profile)
    return shopping_bag


@login_required
def shopping_bag(request, **kwargs):
    shopping_bag = get_shopping_bag(request)
    context = {'shopping_bag': shopping_bag}
    return render(request, 'shopping/shopping_bag.html', context)


@login_required
def add_to_bag(request, **kwargs):
    shopping_bag = get_shopping_bag(request)
    item_to_order = get_object_or_404(Item, pk=kwargs.get('item_pk'))
    order_item, created = OrderItem.objects.get_or_create(item=item_to_order)
    shopping_bag.items.add(order_item)
    shopping_bag.save()
    messages.info(request, 'Item has been added to your shopping bag!')
    return redirect('boutique:item', kwargs.get('item_pk'))


@login_required
def del_from_bag(request, **kwargs):
    shopping_bag = get_shopping_bag(request)
    order_item_to_del = get_object_or_404(
        OrderItem, pk=kwargs.get('order_item_pk'))
    shopping_bag.items.remove(order_item_to_del)
    messages.info(request, 'Item has been removed from your shopping bag!')
    return redirect('shopping:shopping-bag')


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'shopping/orders.html'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        qs = Order.objects.filter(profile=profile, is_ordered=True)
        return qs


@method_decorator(login_required, name='dispatch')
class OrderDetailView(ListView):
    model = Order
    template_name = 'shopping/order.html'


@login_required
def handle_order(request, **kwargs):
    order = get_shopping_bag(request)
    order.ref_number = ref_number_generator()
    order.is_ordered = True
    order.active = True
    order.save()

    # send an email to admin

    messages.info(
        request, 'Your order has been placed! Our staff will contact you within 24 hours. Or you can contact us directly: +7 (925) 519-62-42. Thank you!')
    return redirect('shopping:show-order', order.pk)


def buy_now(request, **kwargs):
    """ 
    place order without signing in:
    - fill in forms: email, name, city, phone number
    - new order obj: assign item, generate ref_number
    - send email to the customer and admin
    """
    item_pk = kwargs.get('item_pk')
    item_to_buy = get_object_or_404(Item, pk=item_pk)

    if request.method == 'POST':
        form = AnonymousOrderForm(data=request.POST)
        if form.is_valid():
            # create the order object
            new_order = form.save(commit=False)
            new_order.item = item_to_buy
            # generate the ref code
            new_order.ref_number = anonymous_ref_number_generator()
            new_order.save()
            # send email to the customer
            messages.info(request, 'Your order is being processed!')
            return redirect('shopping:buy-now-order', item_pk, new_order.ref_number)

    # get an empty form to fill in
    form = AnonymousOrderForm()
    context = {
        'item': item_to_buy,
        'form': form, }
    return render(request, 'shopping/templates/shopping/buy_now.html', context)


def buy_now_order(request, item_pk, order_ref_number):
    """ 
    Display the order just bought
    """
    item_ordered = get_object_or_404(Item, pk=item_pk)
    new_order = get_object_or_404(AnonymousOrder, ref_number=order_ref_number)
    context = {
        'item': item_ordered,
        'order': new_order,
    }
    return render(request, 'shopping/buy_now_order.html', context)


""" FOR REGISTERED USERS ONLY """
@login_required
def buy_now_registered(request, **kwargs):
    """ 
    place order for registered users:
    - load/complete profile info: email, name, city, phone number
    - new order obj: assign item to OrderItem, generate ref_number
    - send email to the customer and admin
    """
    item_pk = kwargs.get('item_pk')
    item_to_buy = get_object_or_404(Item, pk=item_pk)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(data=request.POST)
        if form.is_valid():
            # create the order object
            new_order = form.save(commit=False)
            new_order.items.add(item_to_buy)
            # generate the ref code
            new_order.ref_number = ref_number_generator()
            new_order.is_ordered = True
            new_order.active = True
            new_order.save()
            # send email to the customer
            messages.info(request, 'Your order is being processed!')
            return redirect('shopping:buy-now-order', item_pk, new_order.ref_number)

    # get an empty form to fill in
    form = ProfileForm()
    context = {
        'item': item_to_buy,
        'form': form, }
    return render(request, 'shopping/templates/shopping/buy_now.html', context)
