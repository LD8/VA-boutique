from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import VipOrder
from .forms import VipOrderForm
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from shopping.extras import mail_order_detail

from random import choice
from string import ascii_uppercase
from datetime import date


def vip_ref_number_generator():
    date_str = date.today().strftime('%d%m%y')
    random_str = "".join([choice(ascii_uppercase) for x in range(3)])
    return "VIP{}-{}".format(date_str, random_str)


def create_vip_order(request, **kwargs):
    """ Create a VIP order, taking in at least one image file """

    form = VipOrderForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        new_vip_order = form.save(commit=False)
        new_vip_order.active = True
        new_vip_order.ref_number = vip_ref_number_generator()
        new_vip_order.save()

        # send email to the customer
        kwargs = {
            'new_order_username': 'VIP {}'.format(new_vip_order.name.capitalize()),
            'new_order_ref_number': new_vip_order.ref_number,
            'new_order_item_names': new_vip_order.item_description,
            'customer_email': new_vip_order.email,
            'customer_phone': new_vip_order.phone,
            'new_order_link': request.build_absolute_uri(
                    reverse('vip:vip-order', kwargs={'ref': new_vip_order.ref_number})),
        }
        mail_order_detail(**kwargs)

        messages.success(request, _(
            "Thanks for your purchase, we will contact you soon!"))
        return redirect('vip:vip-order', new_vip_order.ref_number)
   
    context = {
        'form': form,
        'meta': {
            'content': "Купить сумку на заказ. Купить копии сумок на заказ. Реплики известных брендов на заказ со скидкой. Ремни и Очки на заказ. Качественная обувь под заказ",
            'title': "Сумки под заказ. Обувь и ремни под заказ. Реплики",
        },
    }
    return render(request, "vip/create_vip_order.html", context)


def show_vip_order(request, ref):
    """ Display a VIP order """
    vip_order = get_object_or_404(VipOrder, ref_number=ref)
    context = {
        'vip_order': vip_order,
        'meta': {
            'content': "Купить сумку на заказ. Купить копии сумок на заказ. Реплики известных брендов на заказ со скидкой. Ремни и Очки на заказ. Качественная обувь под заказ",
            'title': "Сумки под заказ. Обувь и ремни под заказ. Реплики",
        },
    }
    return render(request, 'vip/vip_order.html', context)