from django.shortcuts import render, get_object_or_404, reverse, redirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Order, OrderItem, AnonymousOrder
from users.models import Profile
from django.contrib import messages
from .extras import ref_number_generator, anonymous_ref_number_generator, mail_order_detail
from .forms import AnonymousOrderForm, ProfileForm
from boutique.models import Item
from django.utils.translation import gettext_lazy as _


def get_shopping_bag(request):
    profile = get_object_or_404(Profile, user=request.user)
    # get pending order as shopping_bag object
    shopping_bag, created = Order.objects.get_or_create(
        is_ordered=False,
        profile=profile,
        ref_number="{}'s shopping bag".format(request.user.username),
    )
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
    messages.info(request, _('Item has been added to your shopping bag!'))
    return redirect('shopping:shopping-bag')


@login_required
def del_from_bag(request, **kwargs):
    shopping_bag = get_shopping_bag(request)
    order_item_to_del = get_object_or_404(
        OrderItem, pk=kwargs.get('order_item_pk'))
    shopping_bag.items.remove(order_item_to_del)
    messages.info(request, _('Item has been removed from your shopping bag!'))
    return redirect('shopping:shopping-bag')


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'shopping/orders.html'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return Order.objects.filter(profile=profile, is_ordered=True)


@login_required
def show_registered_order(request, ref):
    """ Display an order placed by a registered user """
    order = get_object_or_404(Order, ref_number=ref)
    
    # fast track to superuser
    if request.user.is_superuser:
        return render(request, 'shopping/order.html', {'order': order})

    # authentication: user should be the owner of the profile to view their order
    if order.profile != request.user.profile:
        messages.info(request, 'Сожалею! Вы не можете видеть заказы другого участника ...')
        raise Http404
    return render(request, 'shopping/order.html', {'order': order})


@login_required
def handle_order(request, **kwargs):
    order = get_shopping_bag(request)
    if order.items.count == 0:
        messages.info(request, _('Please add more items to your shpping bag'))
        return redirect('shopping:shopping-bag')
    order.ref_number = ref_number_generator()
    order.is_ordered = True
    order.active = True
    order.save()

    kwargs = {
        'new_order_username': request.user.username.capitalize(),
        'new_order_ref_number': order.ref_number,
        'new_order_item_names': ", ".join([item.item.name for item in order.items.all()]),
        'customer_email': order.profile.email,
        'new_order_link': request.build_absolute_uri(
                reverse('shopping:show-order', kwargs={'ref': order.ref_number})),
    }
    mail_order_detail(**kwargs)
    
    messages.info(request, _(
        'Your order is being processed! Please check your profile or your email for the details of the order.'))
    return redirect('shopping:show-order', order.ref_number)


def buy_now_unregistered(request, **kwargs):
    """
    place order without signing in:
    - fill in forms: email, name, address, phone number
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
            kwargs = {
                'new_order_username': 'Unregistered user {}'.format(new_order.customer_name.capitalize()),
                'new_order_ref_number': new_order.ref_number,
                'new_order_item_names': item_to_buy.name,
                'customer_email': new_order.customer_email,
                'new_order_link': request.build_absolute_uri(
                        reverse('shopping:show-unregistered-order', kwargs={'ref': new_order.ref_number})),
            }
            mail_order_detail(**kwargs)

            messages.info(request, _('Your order is being processed!'))
            return redirect('shopping:show-unregistered-order', new_order.ref_number)

    form = AnonymousOrderForm()
    context = {
        'item': item_to_buy,
        'form': form, }
    return render(request, 'shopping/buy_now.html', context)


def show_unregistered_order(request, ref):
    """ Display an order placed by an unregistered user """
    order = get_object_or_404(AnonymousOrder, ref_number=ref)
    return render(request, 'shopping/unregistered_order.html', {'order': order})


""" FOR REGISTERED USERS ONLY """
@login_required
def buy_now_registered(request, **kwargs):
    """
    place order for registered users:
    - load/complete profile info: email, name, address, phone number
    - new order obj: assign item to OrderItem, generate ref_number
    - send email to the customer and admin
    """
    item_pk = kwargs.get('item_pk')
    item_to_buy = get_object_or_404(Item, pk=item_pk)
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            # save profile
            form.save()

            # get or create OrderItem instance
            new_order_item, created = OrderItem.objects.get_or_create(
                item=item_to_buy)

            # create the order object and add ordered item
            new_order = Order.objects.create(profile=profile)
            new_order.items.add(new_order_item)

            # generate the ref code, change order status
            new_order.ref_number = ref_number_generator()
            new_order.is_ordered = True
            new_order.active = True
            new_order.save()

            # send email to the customer
            kwargs = {
                'new_order_username': profile.user.username.capitalize(),
                'new_order_ref_number': new_order.ref_number,
                'new_order_item_names': item_to_buy.name,
                'customer_email': profile.email,
                'new_order_link': request.build_absolute_uri(
                        reverse('shopping:show-order', kwargs={'ref': new_order.ref_number})),
            }
            mail_order_detail(**kwargs)
            
            messages.info(request, _(
                'Your order is being processed! Please check your profile or your email for the details of the order.'))
            return redirect('shopping:show-order', new_order.ref_number)

    # get an empty form to fill in
    form = ProfileForm(instance=profile)
    context = {
        'item': item_to_buy,
        'form': form, }
    return render(request, 'shopping/buy_now.html', context)

